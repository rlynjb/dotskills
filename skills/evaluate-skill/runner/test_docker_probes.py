from dataclasses import replace
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType, SimpleNamespace
import unittest

import docker_policy as dp

try:
    import docker_probes as probes
except ModuleNotFoundError:
    probes = None


def digest(character):
    return character * 64


class FakeDockerRunner:
    def __init__(self, topology, report, *, inspect_change=None, cleanup=None, malformed=False, timeout=False):
        self.topology = topology
        self.report = report
        self.inspect_change = inspect_change
        self.cleanup = cleanup or {"containers": [], "networks": [], "volumes": []}
        self.malformed = malformed
        self.timeout = timeout
        self.seen = []

    def container_payload(self, container, *, probe=False):
        command = ("probe", "--binding", "/run/evaluate/binding.json") if probe else container.command
        value = {
            "Name": "/" + container.name,
            "Config": {
                "Image": container.image,
                "User": container.user,
                "Env": list(container.environment),
                "Entrypoint": list(container.entrypoint),
                "Cmd": list(command),
                "Labels": dict(container.labels),
            },
            "HostConfig": {
                "ReadonlyRootfs": container.read_only_root,
                "Privileged": False,
                "CapDrop": list(container.cap_drop),
                "SecurityOpt": list(container.security_options),
                "NetworkMode": container.networks[0],
                "PidMode": "",
                "IpcMode": "",
                "UTSMode": "",
                "UsernsMode": "",
                "NanoCpus": int(container.cpus * 1_000_000_000),
                "Memory": container.memory_bytes,
                "PidsLimit": container.pids_limit,
                "Tmpfs": dict(container.tmpfs),
            },
            "Mounts": [
                {
                    "Type": mount.kind,
                    "Source": mount.source,
                    "Destination": mount.target,
                    "RW": not mount.read_only,
                    "Propagation": mount.propagation,
                }
                for mount in container.mounts
            ],
            "NetworkSettings": {
                "Networks": {network: {} for network in container.networks}
            },
        }
        if self.inspect_change is not None:
            self.inspect_change(value, container.role)
        return value

    def __call__(self, argv):
        argv = tuple(argv)
        self.seen.append(argv)
        if self.timeout and "--attach" in argv:
            raise TimeoutError("synthetic probe timeout")
        if argv[1:3] == ("network", "inspect"):
            payload = [
                {
                    "Name": self.topology.internal_network.name,
                    "Internal": True,
                    "EnableIPv6": False,
                    "Driver": "bridge",
                    "Attachable": False,
                    "Labels": dict(self.topology.internal_network.labels),
                },
                {
                    "Name": self.topology.egress_network.name,
                    "Internal": False,
                    "EnableIPv6": False,
                    "Driver": "bridge",
                    "Attachable": False,
                    "Labels": dict(self.topology.egress_network.labels),
                },
            ]
            return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr="")
        if argv[1] == "inspect":
            name = argv[-1]
            if name == self.topology.gateway.name:
                payload = [self.container_payload(self.topology.gateway)]
            else:
                payload = [self.container_payload(self.topology.workload, probe=True)]
            return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr="")
        if argv[1:3] == ("start", "--attach"):
            output = "not-json" if self.malformed else json.dumps(self.report)
            return SimpleNamespace(returncode=0, stdout=output, stderr="")
        if argv[1] == "ps":
            return SimpleNamespace(returncode=0, stdout=json.dumps(self.cleanup["containers"]), stderr="")
        if argv[1:3] == ("network", "ls"):
            return SimpleNamespace(returncode=0, stdout=json.dumps(self.cleanup["networks"]), stderr="")
        if argv[1:3] == ("volume", "ls"):
            return SimpleNamespace(returncode=0, stdout=json.dumps(self.cleanup["volumes"]), stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")


class DockerProbeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.fixture = self.root / "prepared" / "fixture"
        self.skill = self.root / "prepared" / "skill"
        self.artifacts = self.root / "host-artifacts"
        self.fixture.mkdir(parents=True)
        self.skill.mkdir()
        self.artifacts.mkdir()
        self.binding = self.artifacts / "binding.json"
        self.gateway_binding = self.artifacts / "gateway-binding.json"
        self.replay = self.artifacts / "replay"
        self.seccomp = self.artifacts / "seccomp.json"
        self.binding.write_text("{}\n", encoding="utf-8")
        self.gateway_binding.write_text("{}\n", encoding="utf-8")
        self.seccomp.write_text("{}\n", encoding="utf-8")
        self.replay.mkdir()
        self.counter = 0

    def require_probes(self):
        self.assertIsNotNone(probes, "docker_probes module must exist")
        return probes

    def topology(self):
        plan_digest = digest("a")
        labels = lambda role: MappingProxyType(
            {
                "evaluate.plan": plan_digest,
                "evaluate.run": "run-001",
                "evaluate.role": role,
                "evaluate.schema": "0.4",
            }
        )
        internal = dp.DockerNetworkPolicy(
            "eval-aaaaaaaaaaaa-run-001-internal",
            True,
            False,
            "bridge",
            False,
            labels("internal-network"),
        )
        egress = dp.DockerNetworkPolicy(
            "eval-aaaaaaaaaaaa-run-001-gateway-egress",
            False,
            False,
            "bridge",
            False,
            labels("gateway-egress-network"),
        )
        security = (
            "no-new-privileges:true",
            "seccomp=" + str(self.seccomp),
        )
        tmpfs = MappingProxyType(
            {"/tmp": "rw,noexec,nosuid,nodev,size=33554432"}
        )
        workload = dp.DockerContainerPolicy(
            role="workload",
            name="eval-aaaaaaaaaaaa-run-001-work-with-skill",
            image="registry.invalid/evaluate-codex@sha256:" + digest("1"),
            user="65532:65532",
            read_only_root=True,
            cap_drop=("ALL",),
            security_options=security,
            networks=(internal.name,),
            mounts=(
                dp.DockerMount("bind", str(self.fixture), "/fixture", True),
                dp.DockerMount("bind", str(self.skill), "/skill", True),
                dp.DockerMount(
                    "bind",
                    str(self.binding),
                    "/run/evaluate/binding.json",
                    True,
                ),
            ),
            tmpfs=tmpfs,
            environment=(
                "EVALUATE_GATEWAY_BASE_URL=http://provider-gateway:8080/v1",
                "EVALUATE_RUN_GRANT=synthetic-short-lived-grant",
            ),
            entrypoint=(
                "/opt/evaluate/bin/python3",
                "/opt/evaluate/codex-entrypoint.py",
            ),
            command=("evaluate", "--binding", "/run/evaluate/binding.json"),
            cpus=1.0,
            memory_bytes=536870912,
            pids_limit=64,
            labels=labels("workload-with-skill"),
        )
        gateway = dp.DockerContainerPolicy(
            role="gateway",
            name="eval-aaaaaaaaaaaa-run-001-gateway",
            image="registry.invalid/evaluate-gateway@sha256:" + digest("2"),
            user="65532:65532",
            read_only_root=True,
            cap_drop=("ALL",),
            security_options=security,
            networks=(internal.name, egress.name),
            mounts=(
                dp.DockerMount(
                    "bind",
                    str(self.gateway_binding),
                    "/run/evaluate/gateway-binding.json",
                    True,
                ),
                dp.DockerMount(
                    "bind",
                    str(self.replay),
                    "/var/lib/evaluate-gateway/replay",
                    False,
                ),
            ),
            tmpfs=tmpfs,
            environment=(),
            entrypoint=(
                "/opt/evaluate/bin/python3",
                "/opt/evaluate/gateway-entrypoint.py",
            ),
            command=(
                "serve",
                "--binding",
                "/run/evaluate/gateway-binding.json",
                "--replay-ledger",
                "/var/lib/evaluate-gateway/replay",
            ),
            cpus=1.0,
            memory_bytes=536870912,
            pids_limit=64,
            labels=labels("gateway"),
        )
        docker = "/reviewed/bin/docker"
        commands = (
            dp.DockerCommand("create-internal-network", "network", (docker, "network", "create", internal.name)),
            dp.DockerCommand("create-egress-network", "network", (docker, "network", "create", egress.name)),
            dp.DockerCommand(
                "create",
                "gateway",
                (docker, "create", "--name", gateway.name, gateway.image, *gateway.command),
            ),
            dp.DockerCommand("connect-egress-network", "gateway", (docker, "network", "connect", egress.name, gateway.name)),
            dp.DockerCommand("inspect-networks", "network", (docker, "network", "inspect", internal.name, egress.name)),
            dp.DockerCommand("inspect", "gateway", (docker, "inspect", gateway.name)),
            dp.DockerCommand(
                "create",
                "workload",
                (docker, "create", "--name", workload.name, workload.image, *workload.command),
            ),
            dp.DockerCommand("inspect", "workload", (docker, "inspect", workload.name)),
            dp.DockerCommand("start", "gateway", (docker, "start", gateway.name)),
            dp.DockerCommand("start", "workload", (docker, "start", workload.name)),
            dp.DockerCommand("stop", "workload", (docker, "stop", workload.name)),
            dp.DockerCommand("stop", "gateway", (docker, "stop", gateway.name)),
            dp.DockerCommand("rm", "workload", (docker, "rm", "--force", workload.name)),
            dp.DockerCommand("rm", "gateway", (docker, "rm", "--force", gateway.name)),
            dp.DockerCommand("remove-networks", "network", (docker, "network", "rm", internal.name, egress.name)),
        )
        limits = MappingProxyType(
            {
                "max_seconds": 120,
                "max_turns": 10,
                "max_output_bytes": 200000,
                "max_cost_usd": 1.0,
                "max_cpus": 1.0,
                "max_memory_bytes": 536870912,
                "max_pids": 64,
                "max_tmpfs_bytes": 33554432,
            }
        )
        return dp.DockerRunTopology(
            "0.4",
            plan_digest,
            "run-001",
            "with-skill",
            internal,
            egress,
            workload,
            gateway,
            limits,
            120,
            200000,
            commands,
        )

    def report(self, topology):
        executable_paths = [
            "/opt/evaluate/bin/python3",
            "/opt/evaluate/bin/node",
            "/opt/evaluate/bin/codex",
            "/opt/evaluate/bin/promptfoo",
        ]
        return {
            "schema_version": "0.4",
            "status": "OBSERVED",
            "plan_digest": topology.plan_digest,
            "observations": {
                "forbidden_paths": {
                    name: "DENIED"
                    for name in (
                        "host_home",
                        "original_repo",
                        "provider_auth",
                        "rubric",
                        "docker_socket",
                        "outside_mount",
                    )
                },
                "writes": {"root": "DENIED", "fixture": "DENIED"},
                "network": {
                    "direct_egress": "DENIED",
                    "host_service": "DENIED",
                    "metadata": "DENIED",
                    "unapproved_sidecar": "DENIED",
                },
                "runtime": {
                    "uid": 65532,
                    "gid": 65532,
                    "no_new_privileges": True,
                    "seccomp": "FILTERED",
                    "effective_capabilities": "0",
                    "host_namespaces": False,
                },
                "inventory": {
                    "executables": executable_paths,
                    "processes": ["/opt/evaluate/bin/python3"],
                    "forbidden_executables": [],
                },
                "tools": {
                    "allowed_tools": ["list", "read", "search"],
                    "bounded": True,
                    "decisions": [
                        ["list", "/fixture", "ALLOWED"],
                        ["read", "/fixture/sample.txt", "ALLOWED"],
                        ["search", "/fixture", "ALLOWED"],
                        ["read", "/etc/passwd", "DENIED"],
                        ["read", "/fixture-link", "DENIED"],
                    ],
                },
            },
        }

    def inventory(self):
        return {
            "schema_version": "0.4",
            "status": "verified",
            "target_platform": "linux/arm64",
            "allowed_tools": ["list", "read", "search"],
            "executables": [
                {"path": path, "role": "approved", "digest": digest(character)}
                for path, character in zip(
                    (
                        "/opt/evaluate/bin/python3",
                        "/opt/evaluate/bin/node",
                        "/opt/evaluate/bin/codex",
                        "/opt/evaluate/bin/promptfoo",
                    ),
                    ("3", "4", "5", "6"),
                )
            ],
            "scripts": [
                {
                    "path": "/opt/evaluate/codex-entrypoint.py",
                    "interpreter": "/opt/evaluate/bin/python3",
                    "digest": digest("7"),
                },
                {
                    "path": "/opt/evaluate/probe-entrypoint.py",
                    "interpreter": "/opt/evaluate/bin/python3",
                    "digest": digest("8"),
                },
            ],
        }

    def canaries(self):
        return {
            "forbidden_paths": {
                "host_home": "/host-canaries/home",
                "original_repo": "/host-canaries/repository",
                "provider_auth": "/host-canaries/provider-auth.json",
                "rubric": "/host-canaries/rubric.json",
                "docker_socket": "/host-canaries/docker.sock",
                "outside_mount": "/host-canaries/outside",
            },
            "credential_canary": "never-persist-this-provider-secret",
            "protected_state_before": digest("9"),
            "protected_state_after": digest("9"),
            "fixture_state_before": digest("a"),
            "fixture_state_after": digest("a"),
            "grant_present_before": True,
            "grant_present_after": False,
        }

    def gateway(self, **changes):
        value = {
            "valid_synthetic_request": "ALLOWED",
            "wrong_nonce": "DENIED",
            "wrong_provider": "DENIED",
            "wrong_model": "DENIED",
            "wrong_role": "DENIED",
            "over_budget": "DENIED",
            "expired": "DENIED",
            "credential_retrieval": "DENIED",
            "direct_destination": "DENIED",
            "real_credential_exposed": False,
            "provider_called": False,
        }
        value.update(changes)
        return lambda: value

    def artifact_directory(self):
        self.counter += 1
        path = self.root / f"preflight-{self.counter}"
        path.mkdir()
        return path

    def preflight(
        self,
        *,
        topology=None,
        report=None,
        runner=None,
        gateway=None,
        canaries=None,
        inventory=None,
        artifact_directory=None,
    ):
        module = self.require_probes()
        topology = self.topology() if topology is None else topology
        report = self.report(topology) if report is None else report
        runner = FakeDockerRunner(topology, report) if runner is None else runner
        return module.run_docker_preflight(
            topology,
            runner=runner,
            gateway_probe=self.gateway() if gateway is None else gateway,
            host_canaries=self.canaries() if canaries is None else canaries,
            executable_inventory=self.inventory() if inventory is None else inventory,
            runtime_digest=digest("b"),
            image_digest=digest("1"),
            gateway_policy_digest=digest("c"),
            fixture_digest=digest("d"),
            observer_policy_digest=digest("e"),
            artifact_directory=(
                self.artifact_directory()
                if artifact_directory is None
                else artifact_directory
            ),
        )

    def result(self, preflight, probe_id):
        return {item.probe_id: item for item in preflight.results}[probe_id]

    def test_preflight_requires_exact_complete_probe_set(self):
        preflight = self.preflight()

        self.assertEqual(preflight.status, "READY_NOT_RUN")
        self.assertFalse(preflight.model_executed)
        self.assertEqual(
            {item.probe_id for item in preflight.results},
            set(self.require_probes().REQUIRED_DOCKER_PROBES),
        )
        self.assertTrue(all(item.status == "PASS" for item in preflight.results))
        self.assertTrue(preflight.artifact_path.is_file())
        persisted = preflight.artifact_path.read_text(encoding="utf-8")
        self.assertNotIn(self.canaries()["credential_canary"], persisted)
        with self.assertRaises(self.require_probes().DockerProbeError):
            self.preflight(artifact_directory=preflight.artifact_path.parent)

    def test_probe_denies_host_home_repo_auth_rubric_socket_and_outside_mounts(self):
        topology = self.topology()
        report = self.report(topology)
        report["observations"]["forbidden_paths"]["docker_socket"] = "ALLOWED"
        preflight = self.preflight(report=report)

        self.assertEqual(preflight.status, "BLOCKED_NOT_RUN")
        self.assertEqual(self.result(preflight, "docker-mount-boundary").status, "FAIL")

        outside_mount = dp.DockerMount("bind", "/host-canaries/home", "/leak", True)
        changed_workload = replace(
            topology.workload,
            mounts=topology.workload.mounts + (outside_mount,),
        )
        topology = replace(topology, workload=changed_workload)
        runner = FakeDockerRunner(topology, self.report(topology))
        preflight = self.preflight(
            topology=topology,
            runner=runner,
            report=self.report(topology),
        )
        self.assertEqual(self.result(preflight, "docker-mount-boundary").status, "FAIL")

    def test_probe_denies_root_and_fixture_writes_for_readonly_profile(self):
        topology = self.topology()
        report = self.report(topology)
        report["observations"]["writes"]["fixture"] = "ALLOWED"
        preflight = self.preflight(report=report)

        self.assertEqual(self.result(preflight, "docker-readonly-filesystem").status, "FAIL")

    def test_probe_denies_direct_egress_host_metadata_and_unapproved_sidecars(self):
        topology = self.topology()
        report = self.report(topology)
        report["observations"]["network"]["metadata"] = "ALLOWED"
        preflight = self.preflight(report=report)

        self.assertEqual(self.result(preflight, "docker-network-boundary").status, "FAIL")

    def test_probe_rejects_wrong_gateway_scope_and_credential_retrieval(self):
        preflight = self.preflight(gateway=self.gateway(wrong_model="ALLOWED"))
        self.assertEqual(
            self.result(preflight, "docker-gateway-credential-isolation").status,
            "FAIL",
        )
        self.assertFalse(preflight.model_executed)

    def test_probe_confirms_nonroot_caps_seccomp_namespaces_and_resource_limits(self):
        def mutate(payload, role):
            if role == "workload":
                payload["Config"]["User"] = "0:0"
                payload["HostConfig"]["PidsLimit"] = 0

        topology = self.topology()
        runner = FakeDockerRunner(topology, self.report(topology), inspect_change=mutate)
        preflight = self.preflight(runner=runner)

        self.assertEqual(self.result(preflight, "docker-observer-completeness").status, "FAIL")
        self.assertEqual(self.result(preflight, "docker-executable-inventory").status, "FAIL")

    def test_probe_confirms_shell_interpreters_forbidden_executables_absent_and_process_inventory_exact(self):
        topology = self.topology()
        report = self.report(topology)
        report["observations"]["inventory"]["forbidden_executables"] = ["/bin/sh"]
        preflight = self.preflight(report=report)
        self.assertEqual(self.result(preflight, "docker-executable-inventory").status, "FAIL")

        inventory = self.inventory()
        inventory["status"] = "unverified"
        preflight = self.preflight(inventory=inventory)
        self.assertEqual(self.result(preflight, "docker-executable-inventory").status, "FAIL")

    def test_probe_allows_only_bounded_list_read_and_search_tool_decisions(self):
        topology = self.topology()
        report = self.report(topology)
        report["observations"]["tools"]["allowed_tools"].append("shell")
        preflight = self.preflight(report=report)
        self.assertEqual(self.result(preflight, "docker-tool-broker").status, "FAIL")

        path = Path(__file__).with_name("docker") / "probe-entrypoint.py"
        spec = importlib.util.spec_from_file_location("docker_probe_entrypoint", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.authorize_tool("read", "/fixture/file.txt"), "ALLOWED")
        self.assertEqual(module.authorize_tool("read", "/etc/passwd"), "DENIED")
        self.assertEqual(module.authorize_tool("shell", "/fixture"), "DENIED")

    def test_probe_verifies_container_volume_network_grant_and_state_cleanup(self):
        topology = self.topology()
        runner = FakeDockerRunner(
            topology,
            self.report(topology),
            cleanup={"containers": [topology.workload.name], "networks": [], "volumes": []},
        )
        preflight = self.preflight(runner=runner)
        self.assertEqual(self.result(preflight, "docker-cleanup").status, "FAIL")

        canaries = self.canaries()
        canaries["protected_state_after"] = digest("f")
        canaries["grant_present_after"] = True
        preflight = self.preflight(canaries=canaries)
        self.assertEqual(self.result(preflight, "docker-protected-state").status, "FAIL")
        self.assertEqual(self.result(preflight, "docker-cleanup").status, "FAIL")

    def test_failed_unknown_timed_out_or_malformed_probe_is_blocked_not_run(self):
        topology = self.topology()
        report = self.report(topology)
        report["status"] = "PASS"
        report["observations"]["writes"]["root"] = "ALLOWED"
        preflight = self.preflight(report=report)
        self.assertEqual(preflight.status, "BLOCKED_NOT_RUN")
        self.assertEqual(self.result(preflight, "docker-readonly-filesystem").status, "FAIL")

        for runner in (
            FakeDockerRunner(topology, self.report(topology), malformed=True),
            FakeDockerRunner(topology, self.report(topology), timeout=True),
        ):
            with self.subTest(runner=runner):
                preflight = self.preflight(runner=runner)
                self.assertEqual(preflight.status, "BLOCKED_NOT_RUN")
                self.assertTrue(any(item.status in ("UNKNOWN", "INCOMPLETE") for item in preflight.results))
                self.assertFalse(preflight.model_executed)


if __name__ == "__main__":
    unittest.main()
