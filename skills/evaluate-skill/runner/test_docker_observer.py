from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
import unittest

import docker_policy as dp

try:
    import docker_observer as observer
except ModuleNotFoundError:
    observer = None


def digest(character):
    return character * 64


def build_topology(root: Path) -> dp.DockerRunTopology:
    plan_digest = digest("a")

    def labels(role):
        return MappingProxyType(
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
    security = ("no-new-privileges:true", "seccomp=" + str(root / "seccomp.json"))
    tmpfs = MappingProxyType({"/tmp": "rw,noexec,nosuid,nodev,size=33554432"})
    workload = dp.DockerContainerPolicy(
        "workload",
        "eval-aaaaaaaaaaaa-run-001-work-with-skill",
        "registry.invalid/evaluate-codex@sha256:" + digest("1"),
        "65532:65532",
        True,
        ("ALL",),
        security,
        (internal.name,),
        (),
        tmpfs,
        (
            "EVALUATE_GATEWAY_BASE_URL=http://provider-gateway:8080/v1",
            "EVALUATE_RUN_GRANT=short-lived-grant",
        ),
        ("/opt/evaluate/bin/python3", "/opt/evaluate/codex-entrypoint.py"),
        ("evaluate", "--binding", "/run/evaluate/binding.json"),
        1.0,
        536870912,
        64,
        labels("workload-with-skill"),
    )
    gateway = dp.DockerContainerPolicy(
        "gateway",
        "eval-aaaaaaaaaaaa-run-001-gateway",
        "registry.invalid/evaluate-gateway@sha256:" + digest("2"),
        "65532:65532",
        True,
        ("ALL",),
        security,
        (internal.name, egress.name),
        (),
        tmpfs,
        (),
        ("/opt/evaluate/bin/python3", "/opt/evaluate/gateway-entrypoint.py"),
        ("serve", "--binding", "/run/evaluate/gateway-binding.json"),
        1.0,
        536870912,
        64,
        labels("gateway"),
    )
    docker = "/reviewed/bin/docker"
    commands = (
        dp.DockerCommand("create-internal-network", "network", (docker, "network", "create", internal.name)),
        dp.DockerCommand("create-egress-network", "network", (docker, "network", "create", egress.name)),
        dp.DockerCommand("create", "gateway", (docker, "create", gateway.image, *gateway.command)),
        dp.DockerCommand("connect-egress-network", "gateway", (docker, "network", "connect", egress.name, gateway.name)),
        dp.DockerCommand("inspect-networks", "network", (docker, "network", "inspect", internal.name, egress.name)),
        dp.DockerCommand("inspect", "gateway", (docker, "inspect", gateway.name)),
        dp.DockerCommand("create", "workload", (docker, "create", workload.image, *workload.command)),
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


def executable_identities():
    return [
        {
            "image_digest": digest("1"),
            "path": "/opt/evaluate/bin/python3",
            "file_digest": digest("3"),
            "argv_digest": digest("4"),
            "role": "entrypoint-runtime",
            "interpreter_digest": None,
            "script_digest": digest("5"),
        },
        {
            "image_digest": digest("1"),
            "path": "/opt/evaluate/bin/codex",
            "file_digest": digest("6"),
            "argv_digest": digest("7"),
            "role": "provider-harness",
            "interpreter_digest": None,
            "script_digest": None,
        },
    ]


def observer_events(topology, provider_digest=digest("8")):
    timestamp = "2026-11-02T16:30:00Z"

    def event(name, payload):
        return {
            "event_id": "event-" + name,
            "type": name,
            "run_id": topology.run_id,
            "arm": topology.arm,
            "observed_at": timestamp,
            "payload": payload,
        }

    return [
        event("daemon", {"identity_digest": digest("9")}),
        event(
            "containers",
            {
                "workload_name": topology.workload.name,
                "workload_image": topology.workload.image,
                "gateway_name": topology.gateway.name,
                "gateway_image": topology.gateway.image,
            },
        ),
        event(
            "networks",
            {
                "internal": topology.internal_network.name,
                "egress": topology.egress_network.name,
            },
        ),
        event(
            "gateway",
            {
                "session_id": "provider-session-1",
                "provider": "openai",
                "model_version": "approved-snapshot",
                "role": topology.arm,
                "decision": "ALLOW",
                "provider_result_digest": provider_digest,
            },
        ),
        event("runtime_processes", {"executables": executable_identities()}),
        event(
            "provider_session",
            {
                "session_id": "provider-session-1",
                "provider_result_digest": provider_digest,
            },
        ),
        event("provider_result", {"digest": provider_digest}),
        event(
            "tool_decisions",
            {
                "commands": [
                    {
                        "session_id": "provider-session-1",
                        "item_id_digest": digest("a"),
                        "command_digest": digest("b"),
                        "decision": "ALLOW",
                    }
                ]
            },
        ),
        event(
            "lifecycle",
            {"exit_code": 0, "timed_out": False, "output_bytes": 1024},
        ),
        event(
            "cleanup",
            {
                "grant_revoked": True,
                "containers_removed": True,
                "volumes_removed": True,
                "networks_removed": True,
            },
        ),
    ]


class DockerObserverTests(unittest.TestCase):
    STARTED = datetime(2026, 11, 2, 16, 29, tzinfo=timezone.utc)
    COMPLETED = datetime(2026, 11, 2, 16, 31, tzinfo=timezone.utc)

    def require_observer(self):
        self.assertIsNotNone(observer, "docker_observer module must exist")
        return observer

    def observe(self, events=None):
        module = self.require_observer()
        topology = build_topology(Path("/trusted-artifacts"))
        return module.observe_docker_run(
            topology,
            observer_events(topology) if events is None else events,
            daemon_digest=digest("9"),
            provider="openai",
            model_version="approved-snapshot",
            session_id="provider-session-1",
            provider_result_digest=digest("8"),
            approved_executables=executable_identities(),
            observation_started_at=self.STARTED,
            observation_completed_at=self.COMPLETED,
        )

    def test_observer_binds_daemon_container_network_gateway_runtime_processes_and_provider_sessions(self):
        attestation = self.observe()

        self.assertEqual(attestation.safety_status, "PASS")
        self.assertEqual(attestation.daemon_digest, digest("9"))
        self.assertEqual(attestation.provider_session_id, "provider-session-1")
        self.assertEqual(attestation.provider_result_digest, digest("8"))
        self.assertEqual(len(attestation.executable_identities), 2)
        self.assertTrue(attestation.cleanup_complete)
        self.assertRegex(attestation.digest(), r"^[0-9a-f]{64}$")

    def test_executable_identity_binds_image_path_file_argv_role_and_script_digests(self):
        attestation = self.observe()
        identity = attestation.executable_identities[0]

        self.assertEqual(identity.image_digest, digest("1"))
        self.assertEqual(identity.path, "/opt/evaluate/bin/python3")
        self.assertEqual(identity.file_digest, digest("3"))
        self.assertEqual(identity.argv_digest, digest("4"))
        self.assertEqual(identity.role, "entrypoint-runtime")
        self.assertEqual(identity.script_digest, digest("5"))

        topology = build_topology(Path("/trusted-artifacts"))
        events = observer_events(topology)
        events[4]["payload"]["executables"][0]["argv_digest"] = digest("f")
        with self.assertRaises(self.require_observer().DockerObserverError):
            self.observe(events)

    def test_missing_duplicate_cross_run_out_of_window_or_unapproved_event_fails_closed(self):
        topology = build_topology(Path("/trusted-artifacts"))
        variants = []
        missing = observer_events(topology)
        missing.pop()
        variants.append(missing)
        duplicate = observer_events(topology)
        duplicate.append(dict(duplicate[0]))
        variants.append(duplicate)
        cross_run = observer_events(topology)
        cross_run[0]["run_id"] = "other-run"
        variants.append(cross_run)
        outside = observer_events(topology)
        outside[0]["observed_at"] = "2026-11-02T18:00:00Z"
        variants.append(outside)
        unknown = observer_events(topology)
        unknown[0]["type"] = "workload_claimed_safe"
        variants.append(unknown)

        for events in variants:
            with self.subTest(events=events), self.assertRaises(
                self.require_observer().DockerObserverError
            ):
                self.observe(events)


if __name__ == "__main__":
    unittest.main()
