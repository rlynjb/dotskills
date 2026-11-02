from dataclasses import replace
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import docker_contracts as dc

try:
    import provider_gateway as pg
except ModuleNotFoundError:
    pg = None


def digest(character):
    return character * 64


class ProviderGatewayTests(unittest.TestCase):
    KEY = b"g" * 32
    CREDENTIAL = "provider-secret-credential"
    NOW = datetime(2026, 11, 2, 16, 30, tzinfo=timezone.utc)

    def require_gateway(self):
        self.assertIsNotNone(pg, "provider_gateway module must exist")
        return pg

    def binding(self, **changes):
        value = {
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
                "max_requests": 2,
                "max_turns": 2,
                "max_input_bytes": 1024,
                "max_output_bytes": 2048,
                "max_cost_usd": 1.0,
            },
            "issued_at": "2026-11-02T16:00:00Z",
            "expires_at": "2026-11-02T17:00:00Z",
            "single_use_nonce": "single-use-nonce",
            "session_id": "approved-session",
            "gateway_policy_digest": digest("b"),
        }
        value.update(changes)
        return dc.DockerGatewayBinding.from_dict(value)

    def request(self, binding, **changes):
        value = {
            "request_id": "request-1",
            "plan_digest": binding.plan_digest,
            "session_id": binding.session_id,
            "nonce": binding.single_use_nonce,
            "provider": binding.provider,
            "model": binding.model,
            "model_version": binding.model_version,
            "role": binding.role,
            "operation": binding.operation,
            "request_bytes": 128,
            "expected_output_bytes": 512,
            "turn": 1,
            "prompt": "synthetic fixture only",
        }
        value.update(changes)
        return value

    def state(self, module, root):
        ledger = Path(root) / "trusted-gateway-ledger"
        ledger.mkdir()
        return module.GatewayReplayState(ledger)

    def test_grant_is_signed_single_use_expiring_and_plan_bound(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")

        self.assertTrue(grant.verify(binding, self.KEY, at=self.NOW))
        self.assertFalse(
            grant.verify(
                self.binding(plan_digest=digest("c")), self.KEY, at=self.NOW
            )
        )
        self.assertFalse(
            grant.verify(
                binding,
                self.KEY,
                at=datetime(2026, 11, 2, 17, 0, tzinfo=timezone.utc),
            )
        )
        self.assertFalse(replace(grant, signature="0" * 64).verify(binding, self.KEY, at=self.NOW))

    def test_gateway_sibling_allows_only_approved_provider_model_role_operation_and_budget(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")
        observed = {}

        def upstream(endpoint, headers, body):
            observed.update(endpoint=endpoint, headers=dict(headers), body=dict(body))
            return {
                "id": "synthetic-response",
                "model_version": binding.model_version,
                "output": "synthetic answer",
                "usage": {
                    "input_bytes": 128,
                    "output_bytes": 16,
                    "cost_usd": 0.01,
                },
            }

        with TemporaryDirectory() as temp:
            result = module.run_gateway(
                binding,
                grant,
                self.request(binding),
                self.state(module, temp),
                provider_credential=self.CREDENTIAL,
                upstream=upstream,
                grant_key=self.KEY,
                at=self.NOW,
            )

        self.assertTrue(result.decision.allowed)
        self.assertEqual(observed["endpoint"], "https://api.openai.com/v1/responses")
        self.assertEqual(observed["headers"]["authorization"], f"Bearer {self.CREDENTIAL}")
        self.assertEqual(observed["body"]["model"], binding.model)

        changes = (
            {"provider": "anthropic"},
            {"model": "other-model"},
            {"role": "judge"},
            {"operation": "files.delete"},
            {"request_bytes": 1025},
            {"expected_output_bytes": 2049},
            {"turn": 3},
        )
        for change in changes:
            with self.subTest(change=change), TemporaryDirectory() as temp:
                decision = module.authorize_gateway_request(
                    binding,
                    grant,
                    self.request(binding, **change),
                    self.state(module, temp),
                    grant_key=self.KEY,
                    at=self.NOW,
                )
                self.assertFalse(decision.allowed)

    def test_gateway_rejects_wrong_nonce_duplicate_session_expired_or_replayed_grant(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")
        with TemporaryDirectory() as temp:
            state = self.state(module, temp)
            wrong_nonce = module.authorize_gateway_request(
                binding,
                grant,
                self.request(binding, nonce="wrong"),
                state,
                grant_key=self.KEY,
                at=self.NOW,
            )
            self.assertFalse(wrong_nonce.allowed)

            first = module.authorize_gateway_request(
                binding,
                grant,
                self.request(binding),
                state,
                grant_key=self.KEY,
                at=self.NOW,
            )
            self.assertTrue(first.allowed)
            duplicate = module.authorize_gateway_request(
                binding,
                grant,
                self.request(binding),
                state,
                grant_key=self.KEY,
                at=self.NOW,
            )
            self.assertFalse(duplicate.allowed)
            replay = module.authorize_gateway_request(
                binding,
                grant,
                self.request(
                    binding,
                    request_id="request-2",
                    session_id="different-session",
                ),
                state,
                grant_key=self.KEY,
                at=self.NOW,
            )
            self.assertFalse(replay.allowed)

        with TemporaryDirectory() as temp:
            expired = module.authorize_gateway_request(
                binding,
                grant,
                self.request(binding),
                self.state(module, temp),
                grant_key=self.KEY,
                at=datetime(2026, 11, 2, 17, 0, tzinfo=timezone.utc),
            )
            self.assertFalse(expired.allowed)

    def test_gateway_never_returns_or_logs_real_credentials(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")

        def upstream(endpoint, headers, body):
            return {
                "id": "synthetic-response",
                "model_version": binding.model_version,
                "output": f"accidental {self.CREDENTIAL}",
                "credential_echo": self.CREDENTIAL,
                "usage": {
                    "input_bytes": 128,
                    "output_bytes": 32,
                    "cost_usd": 0.01,
                },
            }

        with TemporaryDirectory() as temp:
            result = module.run_gateway(
                binding,
                grant,
                self.request(binding),
                self.state(module, temp),
                provider_credential=self.CREDENTIAL,
                upstream=upstream,
                grant_key=self.KEY,
                at=self.NOW,
            )

        serialized = json.dumps(result.canonical_payload(), sort_keys=True)
        self.assertNotIn(self.CREDENTIAL, serialized)
        event_payloads = [event.canonical_payload() for event in result.events]
        self.assertTrue(all("headers" not in event for event in event_payloads))

    def test_gateway_rejects_arbitrary_proxy_connect_and_unapproved_destination(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")
        changes = (
            {"destination": "https://attacker.invalid"},
            {"host": "attacker.invalid"},
            {"method": "CONNECT"},
            {"headers": {"authorization": "chosen-by-workload"}},
        )
        for change in changes:
            with self.subTest(change=change), TemporaryDirectory() as temp:
                decision = module.authorize_gateway_request(
                    binding,
                    grant,
                    self.request(binding, **change),
                    self.state(module, temp),
                    grant_key=self.KEY,
                    at=self.NOW,
                )
                self.assertFalse(decision.allowed)

    def test_gateway_has_no_ip_forwarding_raw_socket_or_workload_chosen_destination(self):
        module = self.require_gateway()
        contract = module.gateway_container_contract()
        self.assertEqual(
            contract,
            {
                "user": "65532:65532",
                "ip_forwarding": False,
                "raw_socket": False,
                "network_admin": False,
                "workload_chosen_destination": False,
                "provider_endpoint": "https://api.openai.com/v1/responses",
            },
        )

    def test_workload_internal_network_has_no_egress_dns_or_ipv6_bypass(self):
        module = self.require_gateway()
        contract = module.gateway_network_contract()
        self.assertTrue(contract["internal"])
        self.assertFalse(contract["workload_egress"])
        self.assertFalse(contract["workload_dns"])
        self.assertFalse(contract["ipv6"])
        self.assertTrue(contract["gateway_egress"])

    def test_gateway_redacts_prompt_secrets_and_emits_complete_decision_events(self):
        module = self.require_gateway()
        binding = self.binding()
        grant = module.RunGrant.issue(binding, self.KEY, key_id="gateway-key-1")
        prompt_secret = "fixture-secret-marker"

        def upstream(endpoint, headers, body):
            return {
                "id": "synthetic-response",
                "model_version": binding.model_version,
                "output": "safe synthetic answer",
                "usage": {
                    "input_bytes": 128,
                    "output_bytes": 16,
                    "cost_usd": 0.01,
                },
            }

        with TemporaryDirectory() as temp:
            result = module.run_gateway(
                binding,
                grant,
                self.request(binding, prompt=f"review {prompt_secret}"),
                self.state(module, temp),
                provider_credential=self.CREDENTIAL,
                upstream=upstream,
                grant_key=self.KEY,
                at=self.NOW,
            )

        events = [event.canonical_payload() for event in result.events]
        self.assertEqual(
            [event["event_type"] for event in events],
            ["authorization", "upstream-response"],
        )
        serialized = json.dumps(events, sort_keys=True)
        self.assertNotIn(prompt_secret, serialized)
        self.assertIn("prompt_digest", serialized)

    def test_workload_environment_contains_only_run_grant_not_provider_credential(self):
        module = self.require_gateway()
        grant = module.RunGrant.issue(
            self.binding(), self.KEY, key_id="gateway-key-1"
        )
        environment = module.workload_gateway_environment(grant)

        self.assertEqual(
            set(environment), {"EVALUATE_RUN_GRANT", "PROVIDER_BASE_URL"}
        )
        self.assertEqual(
            environment["PROVIDER_BASE_URL"], "http://provider-gateway:8080/v1"
        )
        serialized = json.dumps(dict(environment), sort_keys=True).lower()
        self.assertNotIn(self.CREDENTIAL, serialized)
        self.assertNotIn("api_key", serialized)
        self.assertNotIn("provider_credential", serialized)

    def test_codex_gateway_compatibility_probe_is_synthetic_and_fail_closed(self):
        module = self.require_gateway()
        self.assertTrue(hasattr(module, "probe_codex_gateway_compatibility"))
        calls = []

        def synthetic_gateway(request):
            calls.append(dict(request))
            return {"synthetic": True}

        config = {
            "provider": "openai",
            "adapter": "promptfoo-codex-sdk",
            "base_url": "http://provider-gateway:8080/v1",
            "auth_scheme": "run-grant",
            "direct_egress": False,
        }
        ready = module.probe_codex_gateway_compatibility(config, synthetic_gateway)
        self.assertEqual(ready["status"], "READY_NOT_RUN")
        self.assertFalse(ready["model_executed"])
        self.assertEqual(calls, [{"operation": "compatibility-probe", "model_executed": False}])

        changed = dict(config, direct_egress=True)
        blocked = module.probe_codex_gateway_compatibility(changed, synthetic_gateway)
        self.assertEqual(blocked["status"], "BLOCKED_NOT_RUN")
        self.assertFalse(blocked["model_executed"])

    def test_gateway_image_contract_is_nonroot_fixed_and_shell_free(self):
        root = Path(__file__).with_name("docker")
        dockerfile_path = root / "gateway.Dockerfile"
        entrypoint_path = root / "gateway-entrypoint.py"
        self.assertTrue(dockerfile_path.is_file())
        self.assertTrue(entrypoint_path.is_file())
        dockerfile = dockerfile_path.read_text(encoding="utf-8")
        self.assertIn("USER 65532:65532", dockerfile)
        self.assertIn(
            'ENTRYPOINT ["/opt/evaluate/bin/python3", "/opt/evaluate/gateway-entrypoint.py"]',
            dockerfile,
        )
        self.assertNotIn("RUN ", dockerfile)
        self.assertNotIn("/bin/sh", dockerfile)

        spec = importlib.util.spec_from_file_location(
            "gateway_image_entrypoint", entrypoint_path
        )
        entrypoint = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entrypoint)
        valid = [
            "serve",
            "--binding",
            "/run/evaluate/gateway-binding.json",
            "--replay-ledger",
            "/var/lib/evaluate-gateway/replay",
        ]
        self.assertEqual(
            entrypoint.parse_invocation(valid),
            (
                Path("/run/evaluate/gateway-binding.json"),
                Path("/var/lib/evaluate-gateway/replay"),
            ),
        )
        with self.assertRaises(entrypoint.GatewayEntrypointError):
            entrypoint.parse_invocation(["serve", "--destination", "attacker.invalid"])


if __name__ == "__main__":
    unittest.main()
