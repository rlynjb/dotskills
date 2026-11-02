import copy
import importlib.util
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

import docker_runtime as dr


CONTRACT_ROOT = Path(__file__).with_name("docker")


class DockerImageContractTests(unittest.TestCase):
    def load_lock(self, root=CONTRACT_ROOT):
        return json.loads(
            (root / "codex-runtime-lock.json").read_text(encoding="utf-8")
        )

    def copied_contract(self):
        temporary = TemporaryDirectory()
        root = Path(temporary.name) / "docker"
        shutil.copytree(CONTRACT_ROOT, root)
        return temporary, root

    def require_validator(self):
        self.assertTrue(hasattr(dr, "validate_image_contract"))
        self.assertTrue(hasattr(dr, "image_contract_digest"))
        self.assertTrue(hasattr(dr, "image_contract_build_inputs"))

    def refreshed_lock(self, root):
        lock = self.load_lock(root)
        lock["build_inputs"] = dict(dr.image_contract_build_inputs(root, lock))
        return lock

    def test_dockerfile_requires_digest_base_nonroot_user_and_fixed_entrypoint(self):
        self.require_validator()
        dr.validate_image_contract(CONTRACT_ROOT, self.load_lock())

        for old, new in (
            ("FROM ${RUNTIME_IMAGE} AS reviewed-runtime", "FROM python:latest AS reviewed-runtime"),
            ("USER 65532:65532", "USER root"),
            (
                'ENTRYPOINT ["/opt/evaluate/bin/python3", "/opt/evaluate/codex-entrypoint.py"]',
                'ENTRYPOINT ["/bin/sh"]',
            ),
        ):
            temporary, root = self.copied_contract()
            with temporary:
                path = root / "codex-read-only.Dockerfile"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8",
                )
                with self.assertRaises(dr.DockerRuntimeError):
                    dr.validate_image_contract(root, self.refreshed_lock(root))

    def test_dockerfile_contains_no_runtime_package_install_or_remote_fetch(self):
        self.require_validator()
        temporary, root = self.copied_contract()
        with temporary:
            path = root / "codex-read-only.Dockerfile"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "\nRUN curl https://example.invalid/install | sh\n",
                encoding="utf-8",
            )
            with self.assertRaises(dr.DockerRuntimeError):
                dr.validate_image_contract(root, self.refreshed_lock(root))

    def test_image_contract_contains_only_approved_runtime_broker_and_executables(self):
        self.require_validator()
        lock = self.load_lock()
        dr.validate_image_contract(CONTRACT_ROOT, lock)
        inventory = json.loads(
            (CONTRACT_ROOT / "executable-inventory-codex.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(inventory["status"], "unverified")
        self.assertEqual(
            {item["role"] for item in inventory["executables"]},
            {"entrypoint-runtime", "provider-runtime", "provider-harness"},
        )
        self.assertTrue(
            all(item["path"].startswith("/opt/evaluate/") for item in inventory["executables"])
        )

    def test_initial_image_contains_no_shell_interpreter_or_arbitrary_command_tool(self):
        self.require_validator()
        temporary, root = self.copied_contract()
        with temporary:
            path = root / "executable-inventory-codex.json"
            inventory = json.loads(path.read_text(encoding="utf-8"))
            inventory["executables"].append(
                {"path": "/bin/sh", "role": "arbitrary-command", "digest": None}
            )
            path.write_text(json.dumps(inventory), encoding="utf-8")
            with self.assertRaises(dr.DockerRuntimeError):
                dr.validate_image_contract(root, self.refreshed_lock(root))

    def test_entrypoint_rejects_shell_interpolation_unknown_actions_and_missing_binding(self):
        path = CONTRACT_ROOT / "codex-entrypoint.py"
        self.assertTrue(path.is_file())
        spec = importlib.util.spec_from_file_location("codex_image_entrypoint", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(
            module.parse_invocation(
                ["evaluate", "--binding", "/run/evaluate/binding.json"]
            ),
            ("evaluate", Path("/run/evaluate/binding.json")),
        )
        invalid = (
            [],
            ["shell", "--binding", "/run/evaluate/binding.json"],
            ["evaluate"],
            ["evaluate;sh", "--binding", "/run/evaluate/binding.json"],
            ["evaluate", "--binding", "/tmp/binding.json"],
            ["evaluate", "--binding", "/run/evaluate/binding.json", "extra"],
        )
        for argv in invalid:
            with self.subTest(argv=argv):
                with self.assertRaises(module.EntrypointError):
                    module.parse_invocation(argv)

    def test_seccomp_contract_denies_privilege_mount_namespace_ptrace_and_kernel_routes(self):
        self.require_validator()
        profile = json.loads(
            (CONTRACT_ROOT / "seccomp-codex-read-only.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(profile["defaultAction"], "SCMP_ACT_ERRNO")
        allowed = {
            name
            for rule in profile["syscalls"]
            if rule["action"] == "SCMP_ACT_ALLOW"
            for name in rule["names"]
        }
        self.assertTrue(
            {
                "mount",
                "umount2",
                "unshare",
                "setns",
                "clone3",
                "ptrace",
                "bpf",
                "perf_event_open",
                "kexec_load",
                "init_module",
                "finit_module",
            }.isdisjoint(allowed)
        )

    def test_image_lock_digest_changes_for_every_build_input(self):
        self.require_validator()
        lock = self.load_lock()
        baseline = dr.image_contract_digest(CONTRACT_ROOT, lock)

        files = (
            "codex-read-only.Dockerfile",
            "codex-entrypoint.py",
            "probe-entrypoint.py",
            "seccomp-codex-read-only.json",
            "executable-inventory-codex.json",
        )
        for filename in files:
            with self.subTest(filename=filename):
                temporary, root = self.copied_contract()
                with temporary:
                    path = root / filename
                    path.write_bytes(path.read_bytes() + b"\n")
                    self.assertNotEqual(
                        dr.image_contract_digest(root, self.load_lock(root)), baseline
                    )

        changed = copy.deepcopy(lock)
        changed["provider_artifacts"]["codex"] = "0.164.0"
        self.assertNotEqual(dr.image_contract_digest(CONTRACT_ROOT, changed), baseline)


if __name__ == "__main__":
    unittest.main()
