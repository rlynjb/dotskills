import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType, SimpleNamespace
import unittest

try:
    import docker_runtime as dr
except ModuleNotFoundError:
    dr = None


def digest(character):
    return character * 64


class DockerRuntimeTests(unittest.TestCase):
    def require_runtime(self):
        self.assertIsNotNone(dr, "docker_runtime module must exist")
        return dr

    def runtime_payloads(self):
        return {
            "version": {
                "Client": {"Version": "4.49.0"},
                "Server": {"Version": "28.5.1"},
            },
            "context": {
                "Name": "desktop-linux",
                "Endpoints": {
                    "docker": {
                        "Host": "unix:///Users/evaluator/.docker/run/docker.sock"
                    }
                },
            },
            "info": {
                "OSType": "linux",
                "Architecture": "arm64",
                "Name": "docker-desktop",
            },
        }

    def fake_runner(self, payloads, seen, mutate=None):
        def run(argv):
            seen.append(tuple(argv))
            if mutate is not None:
                mutate(len(seen))
            if argv[1] == "version":
                payload = payloads["version"]
            elif argv[1:3] == ["context", "inspect"]:
                payload = payloads["context"]
            elif argv[1] == "info":
                payload = payloads["info"]
            else:
                self.fail(f"unexpected command: {argv!r}")
            return SimpleNamespace(
                returncode=0, stdout=json.dumps(payload), stderr=""
            )

        return run

    def image_lock_value(self):
        return {
            "schema_version": "0.4",
            "status": "verified",
            "provider": "codex",
            "profile": "read-only",
            "base_image": f"registry.invalid/python-runtime@sha256:{digest('1')}",
            "final_image": f"registry.invalid/evaluate-codex@sha256:{digest('2')}",
            "target_platform": "linux/arm64",
            "build_inputs": {
                "dockerfile": digest("3"),
                "provider_lockfiles": digest("4"),
                "entrypoint": digest("5"),
                "seccomp_profile": digest("6"),
                "executable_inventory": digest("7"),
            },
        }

    def load_lock(self, module, value=None):
        document = self.image_lock_value() if value is None else value
        with TemporaryDirectory() as temp:
            path = Path(temp) / "image-lock.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return module.load_image_lock(path)

    def test_runtime_identity_binds_client_server_context_endpoint_platform_and_executable(self):
        module = self.require_runtime()
        payloads = self.runtime_payloads()
        seen = []
        with TemporaryDirectory() as temp:
            docker = Path(temp) / "docker"
            docker.write_bytes(b"reviewed docker client")
            docker.chmod(0o755)
            identity = module.inspect_docker_runtime(
                docker,
                expected_context="desktop-linux",
                expected_endpoint="unix:///Users/evaluator/.docker/run/docker.sock",
                expected_platform="linux/arm64",
                runner=self.fake_runner(payloads, seen),
            )

        self.assertEqual(identity.client_version, "4.49.0")
        self.assertEqual(identity.server_version, "28.5.1")
        self.assertEqual(identity.context, "desktop-linux")
        self.assertEqual(
            identity.endpoint, "unix:///Users/evaluator/.docker/run/docker.sock"
        )
        self.assertEqual(identity.platform, "linux/arm64")
        self.assertRegex(identity.executable_digest, r"^[0-9a-f]{64}$")
        self.assertEqual(
            [command[1] for command in seen], ["version", "context", "info"]
        )
        self.assertTrue(all(command[0] == identity.executable_path for command in seen))

    def test_runtime_refuses_missing_daemon_remote_tcp_symlink_context_or_platform_drift(self):
        module = self.require_runtime()
        with TemporaryDirectory() as temp:
            root = Path(temp)
            docker = root / "docker"
            docker.write_bytes(b"reviewed docker client")
            docker.chmod(0o755)

            variants = []
            missing_daemon = self.runtime_payloads()
            missing_daemon["version"]["Server"] = None
            variants.append((docker, missing_daemon, "desktop-linux", "unix:///Users/evaluator/.docker/run/docker.sock", "linux/arm64", None))

            remote = self.runtime_payloads()
            remote["context"]["Endpoints"]["docker"]["Host"] = "tcp://remote.invalid:2376"
            variants.append((docker, remote, "desktop-linux", "tcp://remote.invalid:2376", "linux/arm64", None))

            wrong_context = self.runtime_payloads()
            wrong_context["context"]["Name"] = "unexpected"
            variants.append((docker, wrong_context, "desktop-linux", "unix:///Users/evaluator/.docker/run/docker.sock", "linux/arm64", None))

            wrong_platform = self.runtime_payloads()
            wrong_platform["info"]["Architecture"] = "amd64"
            variants.append((docker, wrong_platform, "desktop-linux", "unix:///Users/evaluator/.docker/run/docker.sock", "linux/arm64", None))

            link = root / "docker-link"
            link.symlink_to(docker)
            variants.append((link, self.runtime_payloads(), "desktop-linux", "unix:///Users/evaluator/.docker/run/docker.sock", "linux/arm64", None))

            def mutate(call_number):
                if call_number == 2:
                    docker.write_bytes(b"changed docker client")

            variants.append((docker, self.runtime_payloads(), "desktop-linux", "unix:///Users/evaluator/.docker/run/docker.sock", "linux/arm64", mutate))

            for path, payloads, context, endpoint, platform, mutate_hook in variants:
                with self.subTest(path=path, payloads=payloads, mutate=mutate_hook is not None):
                    docker.write_bytes(b"reviewed docker client")
                    docker.chmod(0o755)
                    with self.assertRaises(module.DockerRuntimeError):
                        module.inspect_docker_runtime(
                            path,
                            expected_context=context,
                            expected_endpoint=endpoint,
                            expected_platform=platform,
                            runner=self.fake_runner(payloads, [], mutate_hook),
                        )

    def test_image_lock_requires_digest_pinned_base_and_final_images(self):
        module = self.require_runtime()
        lock = self.load_lock(module)
        self.assertTrue(lock.base_image.endswith(digest("1")))
        self.assertTrue(lock.final_image.endswith(digest("2")))

        mutations = []
        missing = self.image_lock_value()
        del missing["final_image"]
        mutations.append(missing)
        mutable = self.image_lock_value()
        mutable["base_image"] = "registry.invalid/python-runtime:latest"
        mutations.append(mutable)
        placeholder = self.image_lock_value()
        placeholder["final_image"] = (
            "registry.invalid/evaluate-codex@sha256:" + "0" * 64
        )
        mutations.append(placeholder)

        for value in mutations:
            with self.subTest(value=value):
                with self.assertRaises(module.DockerRuntimeError):
                    self.load_lock(module, value)

    def test_image_lock_binds_dockerfile_lockfiles_entrypoint_seccomp_and_inventory(self):
        module = self.require_runtime()
        lock = self.load_lock(module)
        self.assertIsInstance(lock.build_inputs, MappingProxyType)
        self.assertEqual(
            set(lock.build_inputs),
            {
                "dockerfile",
                "provider_lockfiles",
                "entrypoint",
                "seccomp_profile",
                "executable_inventory",
            },
        )

        for field in lock.build_inputs:
            with self.subTest(field=field):
                value = self.image_lock_value()
                del value["build_inputs"][field]
                with self.assertRaises(module.DockerRuntimeError):
                    self.load_lock(module, value)

    def test_image_inspect_digest_must_match_reviewed_lock(self):
        module = self.require_runtime()
        lock = self.load_lock(module)
        good = [
            {
                "RepoDigests": [lock.final_image],
                "Os": "linux",
                "Architecture": "arm64",
            }
        ]
        module.verify_image_inspect(lock, good)

        for changed in (
            [],
            [{"RepoDigests": [lock.base_image], "Os": "linux", "Architecture": "arm64"}],
            [{"RepoDigests": [lock.final_image], "Os": "linux", "Architecture": "amd64"}],
        ):
            with self.subTest(payload=changed):
                with self.assertRaises(module.DockerRuntimeError):
                    module.verify_image_inspect(lock, changed)


if __name__ == "__main__":
    unittest.main()
