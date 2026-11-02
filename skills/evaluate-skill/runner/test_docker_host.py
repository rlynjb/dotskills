from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

import docker_contracts as dc
import docker_probes as probes
import evidence
from test_docker_observer import (
    build_topology,
    digest,
    executable_identities,
    observer_events,
)

try:
    import docker_host as host
except ModuleNotFoundError:
    host = None


class FakeLifecycleRunner:
    def __init__(self, topology, *, failure=None, output_bytes=32):
        self.topology = topology
        self.failure = failure
        self.output_bytes = output_bytes
        self.calls = []

    def __call__(self, argv, *, timeout_seconds, max_output_bytes):
        argv = tuple(argv)
        self.calls.append((argv, timeout_seconds, max_output_bytes))
        action = argv[1] if len(argv) > 1 else ""
        is_workload_start = action == "start" and self.topology.workload.name in argv
        if self.failure == "timeout" and is_workload_start:
            raise TimeoutError("synthetic timeout")
        if self.failure == "interrupt" and is_workload_start:
            raise KeyboardInterrupt()
        if self.failure == "daemon-loss" and action == "inspect":
            raise ConnectionError("synthetic daemon loss")
        if self.failure == "cleanup" and action == "rm" and self.topology.workload.name in argv:
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b"cleanup failed")
        returncode = 7 if self.failure == "nonzero" and is_workload_start else 0
        if argv[1:3] == ("network", "inspect"):
            stdout = json.dumps(
                [
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
            ).encode("utf-8")
        elif action == "inspect":
            container = (
                self.topology.gateway
                if self.topology.gateway.name in argv
                else self.topology.workload
            )
            stdout = json.dumps([self.container_payload(container)]).encode("utf-8")
        else:
            stdout = b"x" * self.output_bytes if is_workload_start else b""
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=b"")

    def container_payload(self, container):
        return {
            "Name": "/" + container.name,
            "Config": {
                "Image": container.image,
                "User": container.user,
                "Env": list(container.environment),
                "Entrypoint": list(container.entrypoint),
                "Cmd": list(container.command),
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


class DockerHostTests(unittest.TestCase):
    NOW = datetime(2026, 11, 2, 16, 30, tzinfo=timezone.utc)

    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.counter = 0

    def require_host(self):
        self.assertIsNotNone(host, "docker_host module must exist")
        return host

    def topology(self):
        return build_topology(self.root / "host-policies")

    def preflight(self, topology):
        artifact = self.root / "accepted-preflight.json"
        artifact.write_text('{"status":"READY_NOT_RUN"}\n', encoding="utf-8")
        results = tuple(
            probes.DockerProbeResult(
                probe_id=probe_id,
                source="trusted-host",
                status="PASS",
                observation="accepted-no-model-probe",
                evidence_digest=digest(str((index % 9) + 1)),
            )
            for index, probe_id in enumerate(probes.REQUIRED_DOCKER_PROBES)
        )
        payload = artifact.read_bytes()
        return probes.DockerPreflightResult(
            schema_version="0.4",
            status="READY_NOT_RUN",
            model_executed=False,
            plan_digest=topology.plan_digest,
            runtime_digest=digest("b"),
            image_digest=digest("1"),
            topology_digest=topology.digest(),
            probe_topology_digest=digest("c"),
            gateway_policy_digest=digest("d"),
            fixture_digest=digest("e"),
            observer_policy_digest=digest("f"),
            results=results,
            artifact_digest=hashlib.sha256(payload).hexdigest(),
            artifact_path=artifact,
        )

    def authorization(self, topology, preflight):
        return self.require_host().DockerLiveAuthorization.from_dict(
            {
                "schema_version": "0.4",
                "plan_digest": topology.plan_digest,
                "topology_digest": topology.digest(),
                "preflight_digest": preflight.artifact_digest,
                "run_id": topology.run_id,
                "arm": topology.arm,
                "issued_at": "2026-11-02T16:25:00Z",
                "expires_at": "2026-11-02T16:35:00Z",
                "nonce": "fresh-live-authorization",
                "execution_binding_digest": digest("2"),
            }
        )

    def evidence_binding(self, topology):
        return dc.DockerEvidenceBinding.from_dict(
            {
                "schema_version": "0.4",
                "plan_digest": topology.plan_digest,
                "run_nonce": topology.run_id,
                "execution_binding_digest": digest("2"),
                "launch_digest": topology.digest(),
                "gateway_digest": digest("d"),
                "observer_digest": digest("f"),
                "state_digest": digest("6"),
                "cleanup_digest": digest("7"),
            }
        )

    def signing_key(self, artifact_directory):
        path = self.root / "operator" / "evidence.key"
        path.parent.mkdir(exist_ok=True)
        if not path.exists():
            path.write_bytes(b"e" * 32)
            path.chmod(0o600)
        return evidence.load_evidence_signing_key(
            path,
            key_id="evidence-key-1",
            rotation_epoch=4,
            forbidden_roots=(artifact_directory,),
        )

    def artifact_directory(self):
        self.counter += 1
        path = self.root / f"run-artifacts-{self.counter}"
        path.mkdir()
        return path

    def provider_result(self):
        self.counter += 1
        path = self.root / f"provider-result-{self.counter}.json"
        path.write_text(
            json.dumps({"id": "synthetic", "output": "bounded result"}),
            encoding="utf-8",
        )
        return path

    def digest_snapshot(self, topology, preflight):
        return {
            "plan_digest": topology.plan_digest,
            "topology_digest": topology.digest(),
            "preflight_digest": preflight.artifact_digest,
            "runtime_digest": preflight.runtime_digest,
            "image_digest": preflight.image_digest,
            "gateway_policy_digest": preflight.gateway_policy_digest,
            "fixture_digest": preflight.fixture_digest,
            "observer_policy_digest": preflight.observer_policy_digest,
        }

    def supervised(
        self,
        *,
        runner=None,
        revalidate=None,
        revoke_grant=None,
        state_after=None,
        quality_status="PASS",
        publish_hook=None,
        topology=None,
        gateway_key_digest=None,
    ):
        module = self.require_host()
        topology = self.topology() if topology is None else topology
        preflight = self.preflight(topology)
        result_path = self.provider_result()
        result_digest = hashlib.sha256(result_path.read_bytes()).hexdigest()
        events = observer_events(topology, result_digest)
        for event in events:
            if event["type"] == "daemon":
                event["payload"]["identity_digest"] = preflight.runtime_digest
        directory = self.artifact_directory()
        runner = FakeLifecycleRunner(topology) if runner is None else runner
        if hasattr(runner, "output_bytes"):
            for event in events:
                if event["type"] == "lifecycle":
                    event["payload"]["output_bytes"] = runner.output_bytes
        snapshot = self.digest_snapshot(topology, preflight)
        revalidate = (lambda phase: dict(snapshot)) if revalidate is None else revalidate
        revoked = []
        revoke = (lambda: revoked.append(True) or True) if revoke_grant is None else revoke_grant
        signing_key = self.signing_key(directory)
        return module.run_supervised_docker(
            topology,
            preflight=preflight,
            live_authorization=self.authorization(topology, preflight),
            evidence_binding=self.evidence_binding(topology),
            signing_key=signing_key,
            gateway_key_digest=(
                hashlib.sha256(b"g" * 32).hexdigest()
                if gateway_key_digest is None
                else gateway_key_digest
            ),
            runner=runner,
            revalidate=revalidate,
            observer_events=events,
            daemon_digest=preflight.runtime_digest,
            approved_executables=executable_identities(),
            provider="openai",
            model_version="approved-snapshot",
            session_id="provider-session-1",
            provider_result=result_path,
            state_before_digest=digest("6"),
            state_after_digest=digest("6") if state_after is None else state_after,
            artifact_directory=directory,
            revoke_grant=revoke,
            consume_authorization=lambda authorization: True,
            clock=lambda: self.NOW,
            quality_status=quality_status,
            publish_hook=publish_hook,
        )

    def test_supervisor_revalidates_every_digest_immediately_before_create_and_start(self):
        topology = self.topology()
        preflight = self.preflight(topology)
        expected = self.digest_snapshot(topology, preflight)
        phases = []

        def revalidate(phase):
            phases.append(phase)
            value = dict(expected)
            if phase == "before-start":
                value["image_digest"] = digest("9")
            return value

        runner = FakeLifecycleRunner(topology)
        result = self.supervised(
            topology=topology,
            runner=runner,
            revalidate=revalidate,
        )

        self.assertEqual(phases, ["before-create", "before-start"])
        self.assertEqual(result.execution_status, "INCOMPLETE")
        self.assertFalse(
            any(
                call[0][1] == "start" and topology.workload.name in call[0]
                for call in runner.calls
            )
        )

    def test_supervisor_enforces_timeout_output_and_process_limits(self):
        topology = self.topology()
        runner = FakeLifecycleRunner(topology)
        result = self.supervised(topology=topology, runner=runner)

        self.assertEqual(result.execution_status, "COMPLETED")
        self.assertTrue(
            all(call[1] == topology.timeout_seconds for call in runner.calls)
        )
        self.assertTrue(
            all(call[2] == topology.max_output_bytes for call in runner.calls)
        )

        oversized = FakeLifecycleRunner(
            topology, output_bytes=topology.max_output_bytes + 1
        )
        result = self.supervised(topology=topology, runner=oversized)
        self.assertEqual(result.execution_status, "INCOMPLETE")

    def test_timeout_interrupt_nonzero_exit_or_daemon_loss_is_incomplete(self):
        for failure in ("timeout", "interrupt", "nonzero", "daemon-loss"):
            topology = self.topology()
            runner = FakeLifecycleRunner(topology, failure=failure)
            with self.subTest(failure=failure):
                result = self.supervised(topology=topology, runner=runner)
                self.assertEqual(result.execution_status, "INCOMPLETE")
                self.assertNotEqual(result.safety_status, "PASS")

    def test_cleanup_always_revokes_grant_and_removes_containers_volumes_and_network(self):
        topology = self.topology()
        runner = FakeLifecycleRunner(topology, failure="timeout")
        revoked = []
        result = self.supervised(
            topology=topology,
            runner=runner,
            revoke_grant=lambda: revoked.append(True) or True,
        )

        flattened = [call[0] for call in runner.calls]
        self.assertTrue(revoked)
        self.assertTrue(any(argv[1] == "rm" for argv in flattened))
        self.assertTrue(any(argv[1:3] == ("network", "rm") for argv in flattened))
        self.assertTrue(result.cleanup_complete)

    def test_partial_cleanup_preserves_recovery_record_and_never_passes_safety(self):
        topology = self.topology()
        runner = FakeLifecycleRunner(topology, failure="cleanup")
        result = self.supervised(topology=topology, runner=runner)

        self.assertEqual(result.execution_status, "INCOMPLETE")
        self.assertNotEqual(result.safety_status, "PASS")
        self.assertFalse(result.cleanup_complete)
        self.assertTrue(result.recovery_journal.is_file())
        self.assertIsNone(result.receipt)

    def test_gateway_and_evidence_keys_are_distinct_external_and_never_mounted(self):
        topology = self.topology()
        directory = self.artifact_directory()
        key = self.signing_key(directory)
        self.assertTrue(key.path.is_file())
        self.assertFalse(
            any(mount.source == str(key.path) for mount in topology.workload.mounts)
        )

        result = self.supervised(
            topology=topology,
            gateway_key_digest=key.material_digest,
        )
        self.assertEqual(result.execution_status, "BLOCKED")
        self.assertFalse(result.model_may_have_executed)

    def test_crash_recovery_preserves_incomplete_journal_without_resigning(self):
        def crash(_payload):
            raise OSError("synthetic publication crash")

        result = self.supervised(publish_hook=crash)
        self.assertEqual(result.execution_status, "INCOMPLETE")
        self.assertIsNone(result.receipt)
        recovery = self.require_host().load_docker_recovery_journal(
            result.recovery_journal
        )
        self.assertEqual(recovery["status"], "INCOMPLETE")
        self.assertNotIn("signature", recovery)

    def test_quality_cannot_override_failed_or_unknown_safety(self):
        result = self.supervised(
            state_after=digest("9"),
            quality_status="PASS",
        )
        self.assertEqual(result.quality_status, "PASS")
        self.assertEqual(result.safety_status, "FAIL")
        self.assertNotEqual(result.execution_status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
