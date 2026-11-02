import copy
from types import MappingProxyType
import unittest

try:
    import docker_contracts as dc
except ModuleNotFoundError:
    dc = None


def digest(character):
    return character * 64


class DockerContractTests(unittest.TestCase):
    def execution_value(self):
        return {
            "schema_version": "0.4",
            "plan_digest": digest("a"),
            "provider": "openai",
            "profile": "read-only",
            "workload_image": f"registry.invalid/evaluate-codex@sha256:{digest('1')}",
            "workload_image_digest": digest("1"),
            "gateway_image": f"registry.invalid/evaluate-gateway@sha256:{digest('2')}",
            "gateway_image_digest": digest("2"),
            "build_input_digest": digest("3"),
            "runtime_inventory_digest": digest("4"),
            "launch_policy_digest": digest("5"),
            "network_policy_digest": digest("6"),
            "seccomp_policy_digest": digest("7"),
            "gateway_policy_digest": digest("8"),
            "observer_policy_digest": digest("9"),
            "fixture_digest": digest("b"),
            "cleanup_policy_digest": digest("c"),
        }

    def gateway_value(self):
        return {
            "schema_version": "0.4",
            "plan_digest": digest("a"),
            "provider": "openai",
            "provider_version": "0.163.0",
            "adapter": "promptfoo-codex-sdk",
            "adapter_version": "0.125.1",
            "model": "approved-model",
            "model_version": "approved-snapshot",
            "role": "with-skill",
            "operation": "responses.create",
            "limits": {
                "max_sessions": 1,
                "max_requests": 10,
                "max_turns": 10,
                "max_input_bytes": 200000,
                "max_output_bytes": 200000,
                "max_cost_usd": 1.0,
            },
            "issued_at": "2026-11-02T16:00:00Z",
            "expires_at": "2026-11-02T17:00:00Z",
            "single_use_nonce": "docker-run-nonce",
            "session_id": "docker-session",
            "gateway_policy_digest": digest("8"),
        }

    def evidence_value(self):
        return {
            "schema_version": "0.4",
            "plan_digest": digest("a"),
            "run_nonce": "docker-run-nonce",
            "execution_binding_digest": digest("d"),
            "launch_digest": digest("e"),
            "gateway_digest": digest("f"),
            "observer_digest": digest("1"),
            "state_digest": digest("2"),
            "cleanup_digest": digest("3"),
        }

    def require_contracts(self):
        self.assertIsNotNone(dc, "docker_contracts module must exist")
        return dc

    def test_docker_execution_binding_requires_every_security_digest(self):
        module = self.require_contracts()
        binding = module.DockerExecutionBinding.from_dict(self.execution_value())
        self.assertRegex(binding.digest(), r"^[0-9a-f]{64}$")

        required = (
            "workload_image_digest",
            "gateway_image_digest",
            "build_input_digest",
            "runtime_inventory_digest",
            "launch_policy_digest",
            "network_policy_digest",
            "seccomp_policy_digest",
            "gateway_policy_digest",
            "observer_policy_digest",
            "fixture_digest",
            "cleanup_policy_digest",
        )
        for field in required:
            with self.subTest(field=field):
                value = self.execution_value()
                del value[field]
                with self.assertRaises(module.DockerContractError):
                    module.DockerExecutionBinding.from_dict(value)

    def test_docker_binding_rejects_unknown_fields_mutable_tags_and_non_sha256_values(self):
        module = self.require_contracts()
        mutations = []

        unknown = self.execution_value()
        unknown["unexpected"] = True
        mutations.append(unknown)

        mutable = self.execution_value()
        mutable["workload_image"] = "registry.invalid/evaluate-codex:latest"
        mutations.append(mutable)

        uppercase = self.execution_value()
        uppercase["launch_policy_digest"] = "A" * 64
        mutations.append(uppercase)

        mismatch = self.execution_value()
        mismatch["gateway_image_digest"] = digest("4")
        mutations.append(mismatch)

        for value in mutations:
            with self.subTest(value=value):
                with self.assertRaises(module.DockerContractError):
                    module.DockerExecutionBinding.from_dict(value)

    def test_gateway_binding_requires_provider_model_role_budget_expiry_and_single_use_nonce(self):
        module = self.require_contracts()
        binding = module.DockerGatewayBinding.from_dict(self.gateway_value())
        self.assertIsInstance(binding.limits, MappingProxyType)
        self.assertEqual(binding.role, "with-skill")

        mutations = []
        for field in (
            "provider",
            "model",
            "role",
            "expires_at",
            "single_use_nonce",
        ):
            changed = self.gateway_value()
            del changed[field]
            mutations.append(changed)

        bad_budget = self.gateway_value()
        bad_budget["limits"]["max_requests"] = 0
        mutations.append(bad_budget)

        bad_role = self.gateway_value()
        bad_role["role"] = "admin"
        mutations.append(bad_role)

        expired = self.gateway_value()
        expired["expires_at"] = expired["issued_at"]
        mutations.append(expired)

        for value in mutations:
            with self.subTest(value=value):
                with self.assertRaises(module.DockerContractError):
                    module.DockerGatewayBinding.from_dict(value)

    def test_evidence_binding_requires_exact_launch_gateway_observer_state_and_cleanup_digests(self):
        module = self.require_contracts()
        binding = module.DockerEvidenceBinding.from_dict(self.evidence_value())
        self.assertRegex(binding.digest(), r"^[0-9a-f]{64}$")

        for field in (
            "launch_digest",
            "gateway_digest",
            "observer_digest",
            "state_digest",
            "cleanup_digest",
        ):
            with self.subTest(field=field):
                value = self.evidence_value()
                del value[field]
                with self.assertRaises(module.DockerContractError):
                    module.DockerEvidenceBinding.from_dict(value)

        unknown = copy.deepcopy(self.evidence_value())
        unknown["quality_digest"] = digest("4")
        with self.assertRaises(module.DockerContractError):
            module.DockerEvidenceBinding.from_dict(unknown)


if __name__ == "__main__":
    unittest.main()
