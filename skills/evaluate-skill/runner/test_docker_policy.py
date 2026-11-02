from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import unittest

import contracts as c
import docker_contracts as dc
import docker_runtime as dr
import provider_gateway as pg

try:
    import docker_policy as dp
except ModuleNotFoundError:
    dp = None


def digest(character):
    return character * 64


class DockerPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bundle = self.root / "prepared-bundle"
        self.artifacts = self.root / "host-artifacts"
        self.fixture = self.bundle / "fixture"
        self.skill = self.bundle / "skill-snapshot"
        self.workload_binding = self.artifacts / "workload-binding.json"
        self.gateway_binding_path = self.artifacts / "gateway-binding.json"
        self.replay = self.artifacts / "gateway-replay"
        self.seccomp = self.artifacts / "seccomp.json"
        for directory in (self.fixture, self.skill, self.replay):
            directory.mkdir(parents=True)
        for path in (
            self.workload_binding,
            self.gateway_binding_path,
            self.seccomp,
        ):
            path.write_text("{}\n", encoding="utf-8")
        self.seccomp_digest = hashlib.sha256(self.seccomp.read_bytes()).hexdigest()

    def require_policy(self):
        self.assertIsNotNone(dp, "docker_policy module must exist")
        return dp

    def plan(self):
        return c.RunPlan.from_dict(
            {
                "schema_version": "0.4",
                "case_id": "read-only-case",
                "case_revision": "case-sha256",
                "rubric_revision": "rubric-sha256",
                "skill_revision": "skill-sha256",
                "fixture_revision": "fixture-sha256",
                "provider": "openai",
                "provider_version": "0.163.0",
                "model": "approved-model",
                "model_version": "approved-snapshot",
                "adapter": "promptfoo-codex-sdk",
                "adapter_version": "0.125.1",
                "backend": "docker",
                "capabilities": {
                    "profile": "read-only",
                    "filesystem_read": ["fixture"],
                    "filesystem_write": [],
                    "shell": False,
                    "network": [],
                    "mock_tools": [],
                    "credentials": [],
                    "side_effects": [],
                    "evidence": ["action-trace", "protected-state"],
                },
                "resource_limits": {
                    "max_seconds": 120,
                    "max_turns": 10,
                    "max_output_bytes": 200000,
                    "max_cost_usd": 1.0,
                    "max_cpus": 1.0,
                    "max_memory_bytes": 536870912,
                    "max_pids": 64,
                    "max_tmpfs_bytes": 33554432,
                },
                "comparison_arms": ["with-skill", "without-skill"],
                "evidence_requirements": ["provider-result", "host-audit"],
                "cleanup_requirements": [
                    "workspace-removed",
                    "state-verified",
                ],
            }
        )

    def binding(self, plan):
        return dc.DockerExecutionBinding.from_dict(
            {
                "schema_version": "0.4",
                "plan_digest": plan.digest(),
                "provider": plan.provider,
                "profile": plan.capabilities.profile,
                "workload_image": (
                    "registry.invalid/evaluate-codex@sha256:" + digest("1")
                ),
                "workload_image_digest": digest("1"),
                "gateway_image": (
                    "registry.invalid/evaluate-gateway@sha256:" + digest("2")
                ),
                "gateway_image_digest": digest("2"),
                "build_input_digest": digest("3"),
                "runtime_inventory_digest": digest("4"),
                "launch_policy_digest": digest("5"),
                "network_policy_digest": digest("6"),
                "seccomp_policy_digest": self.seccomp_digest,
                "gateway_policy_digest": digest("8"),
                "observer_policy_digest": digest("9"),
                "fixture_digest": digest("a"),
                "cleanup_policy_digest": digest("b"),
            }
        )

    def runtime(self):
        return dr.DockerRuntimeIdentity(
            client_version="4.49.0",
            server_version="28.5.1",
            context="desktop-linux",
            endpoint="unix:///Users/evaluator/.docker/run/docker.sock",
            platform="linux/arm64",
            daemon_name="docker-desktop",
            executable_path="/reviewed/bin/docker",
            executable_digest=digest("c"),
        )

    def image_lock(self):
        return dr.ImageLock.from_dict(
            {
                "schema_version": "0.4",
                "status": "verified",
                "provider": "codex",
                "profile": "read-only",
                "base_image": (
                    "registry.invalid/python-runtime@sha256:" + digest("d")
                ),
                "final_image": (
                    "registry.invalid/evaluate-codex@sha256:" + digest("1")
                ),
                "target_platform": "linux/arm64",
                "provider_artifacts": {
                    "codex": "0.163.0",
                    "promptfoo": "0.125.1",
                    "codex_sdk": "0.125.1",
                    "node": "22.23.1",
                    "python": "3.9.6",
                },
                "build_inputs": {
                    "dockerfile": digest("e"),
                    "provider_lockfiles": digest("f"),
                    "entrypoint": digest("a"),
                    "seccomp_profile": self.seccomp_digest,
                    "executable_inventory": digest("4"),
                },
            }
        )

    def gateway_binding(self, plan, arm):
        return dc.DockerGatewayBinding.from_dict(
            {
                "schema_version": "0.4",
                "plan_digest": plan.digest(),
                "provider": plan.provider,
                "provider_version": plan.provider_version,
                "adapter": plan.adapter,
                "adapter_version": plan.adapter_version,
                "model": plan.model,
                "model_version": plan.model_version,
                "role": arm,
                "operation": "responses.create",
                "limits": {
                    "max_sessions": 1,
                    "max_requests": 2,
                    "max_turns": plan.resource_limits["max_turns"],
                    "max_input_bytes": 65536,
                    "max_output_bytes": plan.resource_limits["max_output_bytes"],
                    "max_cost_usd": plan.resource_limits["max_cost_usd"],
                },
                "issued_at": "2026-11-02T16:00:00Z",
                "expires_at": "2026-11-02T17:00:00Z",
                "single_use_nonce": "single-use-nonce-" + arm,
                "session_id": "session-" + arm,
                "gateway_policy_digest": digest("8"),
            }
        )

    def compile(self, arm="with-skill", run_id="run-001", **changes):
        module = self.require_policy()
        plan = self.plan()
        gateway_binding = self.gateway_binding(plan, arm)
        values = {
            "plan": plan,
            "binding": self.binding(plan),
            "runtime": self.runtime(),
            "image_lock": self.image_lock(),
            "arm": arm,
            "prepared_bundle_root": self.bundle,
            "host_artifact_root": self.artifacts,
            "fixture": self.fixture,
            "skill_snapshot": self.skill if arm == "with-skill" else None,
            "workload_binding": self.workload_binding,
            "gateway_binding": self.gateway_binding_path,
            "gateway_replay": self.replay,
            "seccomp_profile": self.seccomp,
            "run_grant": pg.RunGrant.issue(
                gateway_binding, b"g" * 32, key_id="gateway-key-1"
            ),
            "run_id": run_id,
        }
        values.update(changes)
        return module.compile_docker_topology(**values)

    def inspect_payload(self, container):
        mounts = [
            {
                "Type": mount.kind,
                "Source": mount.source,
                "Destination": mount.target,
                "RW": not mount.read_only,
                "Propagation": mount.propagation,
            }
            for mount in container.mounts
        ]
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
            "Mounts": mounts,
            "NetworkSettings": {
                "Networks": {name: {} for name in container.networks}
            },
        }

    def test_topology_uses_unique_internal_and_gateway_egress_networks(self):
        first = self.compile(run_id="run-001")
        second = self.compile(run_id="run-002")

        self.assertNotEqual(first.internal_network.name, first.egress_network.name)
        self.assertNotEqual(first.internal_network.name, second.internal_network.name)
        self.assertTrue(first.internal_network.internal)
        self.assertFalse(first.egress_network.internal)
        self.assertEqual(first.internal_network.driver, "bridge")
        self.assertFalse(first.internal_network.attachable)
        self.assertEqual(first.internal_network.labels["evaluate.plan"], first.plan_digest)
        self.assertIn(first.plan_digest[:12], first.internal_network.name)

        payload = [
            {
                "Name": first.internal_network.name,
                "Internal": True,
                "EnableIPv6": False,
                "Driver": "bridge",
                "Attachable": False,
                "Labels": dict(first.internal_network.labels),
            },
            {
                "Name": first.egress_network.name,
                "Internal": False,
                "EnableIPv6": False,
                "Driver": "bridge",
                "Attachable": False,
                "Labels": dict(first.egress_network.labels),
            },
        ]
        self.require_policy().verify_effective_network(payload, first)
        payload[0]["Internal"] = False
        with self.assertRaises(self.require_policy().DockerPolicyError):
            self.require_policy().verify_effective_network(payload, first)

    def test_only_gateway_is_dual_homed_and_workloads_have_no_external_route(self):
        topology = self.compile()

        self.assertEqual(
            topology.workload.networks, (topology.internal_network.name,)
        )
        self.assertEqual(
            topology.gateway.networks,
            (topology.internal_network.name, topology.egress_network.name),
        )
        self.assertTrue(topology.internal_network.internal)
        self.assertFalse(topology.internal_network.ipv6)

    def test_workload_is_readonly_nonroot_capdrop_all_no_new_privileges_and_seccomp_bound(self):
        topology = self.compile()
        workload = topology.workload

        self.assertTrue(workload.read_only_root)
        self.assertEqual(workload.user, "65532:65532")
        self.assertEqual(workload.cap_drop, ("ALL",))
        self.assertIn("no-new-privileges:true", workload.security_options)
        self.assertIn("seccomp=" + str(self.seccomp), workload.security_options)

    def test_only_exact_fixture_skill_binding_tmpfs_and_runtime_mounts_are_present(self):
        topology = self.compile()

        self.assertEqual(
            {(mount.source, mount.target, mount.read_only) for mount in topology.workload.mounts},
            {
                (str(self.fixture), "/fixture", True),
                (str(self.skill), "/skill", True),
                (str(self.workload_binding), "/run/evaluate/binding.json", True),
            },
        )
        self.assertEqual(
            dict(topology.workload.tmpfs),
            {
                "/tmp": (
                    "rw,noexec,nosuid,nodev,size="
                    + str(int(topology.resource_limits["max_tmpfs_bytes"]))
                )
            },
        )
        self.assertTrue(
            all(mount.propagation == "rprivate" for mount in topology.workload.mounts)
        )

    def test_docker_socket_home_repo_auth_rubric_and_host_namespaces_are_absent(self):
        topology = self.compile()
        serialized = "\n".join(
            argument for command in topology.commands for argument in command.argv
        ).lower()

        for forbidden in (
            "docker.sock",
            str(Path.home()).lower(),
            "/users/rein/public/dotskills",
            "openai_api_key",
            "authorization",
            "rubric",
            "--privileged",
            "--network=host",
            "--pid=host",
            "--ipc=host",
            "--uts=host",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_cpu_memory_pids_timeout_output_and_tmpfs_limits_match_plan(self):
        topology = self.compile()
        plan = self.plan()

        self.assertEqual(topology.resource_limits, plan.resource_limits)
        self.assertEqual(topology.workload.cpus, plan.resource_limits["max_cpus"])
        self.assertEqual(
            topology.workload.memory_bytes,
            plan.resource_limits["max_memory_bytes"],
        )
        self.assertEqual(topology.workload.pids_limit, plan.resource_limits["max_pids"])
        self.assertEqual(topology.timeout_seconds, plan.resource_limits["max_seconds"])
        self.assertEqual(topology.max_output_bytes, plan.resource_limits["max_output_bytes"])
        incomplete = plan.canonical_payload()
        del incomplete["resource_limits"]["max_pids"]
        with self.assertRaises(c.ContractError):
            c.RunPlan.from_dict(incomplete)

    def test_with_skill_and_without_skill_differ_only_by_approved_skill_mount(self):
        with_skill = self.compile(arm="with-skill")
        without_skill = self.compile(arm="without-skill")

        self.assertEqual(with_skill.workload.security_payload(), without_skill.workload.security_payload())
        with_mounts = {mount.target for mount in with_skill.workload.mounts}
        without_mounts = {mount.target for mount in without_skill.workload.mounts}
        self.assertEqual(with_mounts - without_mounts, {"/skill"})
        self.assertEqual(without_mounts - with_mounts, set())

    def test_symlink_mount_propagation_privileged_host_network_extra_env_or_tag_blocks(self):
        module = self.require_policy()
        symlink = self.bundle / "fixture-link"
        symlink.symlink_to(self.fixture, target_is_directory=True)
        with self.assertRaises(module.DockerPolicyError):
            self.compile(fixture=symlink)
        with self.assertRaises(module.DockerPolicyError):
            self.compile(fixture=Path("relative-fixture"))
        outside = self.root / "outside"
        outside.mkdir()
        with self.assertRaises(module.DockerPolicyError):
            self.compile(fixture=outside)
        with self.assertRaises(module.DockerPolicyError):
            self.compile(host_artifact_root=self.bundle)
        with self.assertRaises(module.DockerPolicyError):
            self.compile(host_artifact_root=Path.home())
        with self.assertRaises(module.DockerPolicyError):
            self.compile(
                binding=replace(
                    self.binding(self.plan()),
                    workload_image="registry.invalid/evaluate-codex:latest",
                )
            )

        topology = self.compile()
        payload = self.inspect_payload(topology.workload)
        mutations = []
        changed = self.inspect_payload(topology.workload)
        changed["Mounts"][0]["Propagation"] = "shared"
        mutations.append(changed)
        changed = self.inspect_payload(topology.workload)
        changed["HostConfig"]["Privileged"] = True
        mutations.append(changed)
        changed = self.inspect_payload(topology.workload)
        changed["HostConfig"]["NetworkMode"] = "host"
        mutations.append(changed)
        changed = self.inspect_payload(topology.workload)
        changed["HostConfig"]["PidMode"] = "host"
        mutations.append(changed)
        changed = self.inspect_payload(topology.workload)
        changed["Config"]["Env"].append("HOME=/host")
        mutations.append(changed)
        changed = self.inspect_payload(topology.workload)
        changed["Config"]["Image"] = "registry.invalid/evaluate-codex:latest"
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed), self.assertRaises(module.DockerPolicyError):
                module.verify_effective_container(changed, topology, "workload")
        module.verify_effective_container(payload, topology, "workload")

    def test_commands_are_argv_without_shell_and_names_are_plan_bound(self):
        topology = self.compile(run_id="Approved_Run-01")

        self.assertIsInstance(topology.commands, tuple)
        for command in topology.commands:
            self.assertIsInstance(command.argv, tuple)
            self.assertEqual(command.argv[0], self.runtime().executable_path)
            self.assertNotIn("sh", command.argv)
            self.assertNotIn("bash", command.argv)
            self.assertFalse(any("$(" in argument or "`" in argument for argument in command.argv))
        for name in (
            topology.internal_network.name,
            topology.egress_network.name,
            topology.workload.name,
            topology.gateway.name,
        ):
            self.assertIn(topology.plan_digest[:12], name)
            self.assertIn("approved-run-01", name)

        network_payload = [
            {
                "Name": topology.internal_network.name,
                "Internal": True,
                "EnableIPv6": False,
                "Driver": "bridge",
                "Attachable": False,
                "Labels": dict(topology.internal_network.labels),
            },
            {
                "Name": topology.egress_network.name,
                "Internal": False,
                "EnableIPv6": False,
                "Driver": "bridge",
                "Attachable": False,
                "Labels": dict(topology.egress_network.labels),
            },
        ]
        self.require_policy().verify_effective_network(network_payload, topology)


if __name__ == "__main__":
    unittest.main()
