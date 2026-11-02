from copy import deepcopy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import contracts as c
import provider_trace as p


class ProviderTraceTests(unittest.TestCase):
    def plan(self):
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": "trusted-trace-case",
            "case_revision": "case-sha256",
            "rubric_revision": "rubric-sha256",
            "skill_revision": "skill-sha256",
            "fixture_revision": "fixture-sha256",
            "provider": "openai",
            "provider_version": "0.163.0",
            "model": "gpt-5",
            "model_version": "gpt-5-2026-10-01",
            "adapter": "promptfoo-codex-sdk",
            "adapter_version": "0.125.1",
            "backend": "native",
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
            },
            "comparison_arms": ["with-skill", "without-skill"],
            "evidence_requirements": ["provider-result", "host-audit"],
            "cleanup_requirements": ["workspace-removed", "state-verified"],
        })

    def promptfoo_config(self):
        return {
            "description": "Evaluate Skill synthetic case trusted-trace-case",
            "prompts": ["{{question}}"],
            "providers": [
                {
                    "id": "openai:codex-sdk",
                    "label": "with_skill",
                    "config": {"model": "gpt-5-2026-10-01"},
                },
                {
                    "id": "openai:codex-sdk",
                    "label": "without_skill",
                    "config": {"model": "gpt-5-2026-10-01"},
                },
            ],
            "tests": [{"vars": {"question": "Inspect the fixture."}, "assert": []}],
            "commandLineOptions": {"share": False, "cache": False},
        }

    def result(self, label, session_id, *, items=None):
        answer = f"answer from {label}"
        if items is None:
            items = [
                {
                    "id": f"reason-{label}",
                    "type": "reasoning",
                    "text": "inspected the fixture",
                },
                {
                    "id": f"message-{label}",
                    "type": "agent_message",
                    "text": answer,
                },
            ]
        turn = {
            "items": items,
            "finalResponse": answer,
            "usage": {"input_tokens": 10, "output_tokens": 5},
        }
        return {
            "promptIdx": 0,
            "testIdx": 0,
            "testCase": {"vars": {"question": "Inspect the fixture."}},
            "promptId": "prompt-sha256",
            "provider": {"id": "openai:codex-sdk", "label": label},
            "prompt": {"raw": "{{question}}", "label": "{{question}}"},
            "vars": {"question": "Inspect the fixture."},
            "response": {
                "output": answer,
                "raw": json.dumps(turn, sort_keys=True),
                "sessionId": session_id,
                "cost": 0.01,
                "tokenUsage": {"prompt": 10, "completion": 5, "total": 15},
            },
            "failureReason": "none",
            "success": True,
            "score": 1.0,
            "latencyMs": 10,
            "gradingResult": {
                "pass": True,
                "score": 1.0,
                "reason": f"quality grade for {label}",
                "namedScores": {"criterion": 1.0},
            },
            "namedScores": {"criterion": 1.0},
        }

    def document(self):
        return {
            "evalId": "eval-trusted-trace",
            "results": {
                "version": 3,
                "timestamp": "2026-11-02T12:00:00.000Z",
                "results": [
                    self.result("with_skill", "session-with"),
                    self.result("without_skill", "session-without"),
                ],
                "prompts": [],
                "stats": {
                    "successes": 2,
                    "failures": 0,
                    "errors": 0,
                    "cacheHits": 0,
                    "tokenUsage": {"prompt": 20, "completion": 10, "total": 30},
                },
            },
            "config": self.promptfoo_config(),
            "shareableUrl": None,
            "metadata": {
                "promptfooVersion": "0.125.1",
                "nodeVersion": "22.23.1",
                "platform": "darwin",
                "arch": "arm64",
                "exportedAt": "2026-11-02T12:01:00.000Z",
            },
            "runtimeOptions": {"cache": False},
        }

    def binding(self):
        plan = self.plan()
        sessions = []
        for arm, session_id in (
            ("with-skill", "session-with"),
            ("without-skill", "session-without"),
        ):
            sessions.append(p.ObservedSessionIdentity(
                arm_name=arm,
                session_id=session_id,
                provider=plan.provider,
                provider_version=plan.provider_version,
                model=plan.model,
                model_version=plan.model_version,
                adapter=plan.adapter,
                adapter_version=plan.adapter_version,
                provider_config_digest="provider-config-sha256",
            ))
        return p.ProviderTraceBinding(
            provider_config_digest="provider-config-sha256",
            promptfoo_config=self.promptfoo_config(),
            observed_sessions=tuple(sessions),
        )

    def parse(self, document, *, binding=None, secrets=()):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "results.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return p.parse_promptfoo_result(
                path,
                self.plan(),
                binding or self.binding(),
                known_secret_values=secrets,
            )

    def assert_rejected(self, document, pattern=None, *, binding=None):
        with self.assertRaises(p.ProviderTraceError) as caught:
            self.parse(document, binding=binding)
        if pattern is not None:
            self.assertIn(pattern, str(caught.exception))

    def test_parser_requires_exactly_one_with_skill_and_one_without_skill_result(self):
        valid = self.document()
        parsed = self.parse(valid)
        self.assertEqual(tuple(arm.arm_name for arm in parsed.arms), (
            "with-skill", "without-skill"
        ))

        for results in (
            valid["results"]["results"][:1],
            valid["results"]["results"] + [deepcopy(valid["results"]["results"][0])],
        ):
            changed = deepcopy(valid)
            changed["results"]["results"] = results
            self.assert_rejected(changed, "exactly two")

        changed = deepcopy(valid)
        changed["results"]["results"][1]["provider"]["label"] = "with_skill"
        self.assert_rejected(changed, "duplicate")

    def test_parser_requires_pinned_provider_model_adapter_and_session_identity(self):
        valid = self.document()
        changed = deepcopy(valid)
        changed["results"]["results"][0]["provider"]["id"] = "openai:chat"
        self.assert_rejected(changed, "provider")

        binding = self.binding()
        wrong = deepcopy(binding.observed_sessions[0])
        object.__setattr__(wrong, "model_version", "drifted-snapshot")
        bad_binding = p.ProviderTraceBinding(
            binding.provider_config_digest,
            binding.promptfoo_config,
            (wrong, binding.observed_sessions[1]),
        )
        self.assert_rejected(valid, "model_version", binding=bad_binding)

        changed = deepcopy(valid)
        changed["results"]["results"][0]["response"]["sessionId"] = "claimed-only"
        self.assert_rejected(changed, "session")

        bad_binding = p.ProviderTraceBinding(
            "different-config-digest",
            binding.promptfoo_config,
            binding.observed_sessions,
        )
        self.assert_rejected(valid, "config digest", binding=bad_binding)

    def test_parser_rejects_cache_hits_missing_raw_turns_or_unknown_schema(self):
        valid = self.document()
        mutations = []

        cached_response = deepcopy(valid)
        cached_response["results"]["results"][0]["response"]["cached"] = True
        mutations.append(cached_response)

        cached_stats = deepcopy(valid)
        cached_stats["results"]["stats"]["cacheHits"] = 1
        mutations.append(cached_stats)

        cached_grade = deepcopy(valid)
        cached_grade["results"]["results"][0]["gradingResult"]["metadata"] = {
            "cachedResponse": True
        }
        mutations.append(cached_grade)

        missing_raw = deepcopy(valid)
        del missing_raw["results"]["results"][0]["response"]["raw"]
        mutations.append(missing_raw)

        unknown = deepcopy(valid)
        unknown["unexpectedRemoteField"] = True
        mutations.append(unknown)

        for document in mutations:
            with self.subTest(document=document):
                self.assert_rejected(document)

    def test_parser_rejects_mcp_web_collaboration_file_change_and_unknown_item_types(self):
        prohibited = (
            "mcp_tool_call",
            "web_search",
            "collaboration_tool_call",
            "file_change",
            "dynamic_tool_call",
            "unrecognized_tool",
        )
        for item_type in prohibited:
            changed = self.document()
            turn = json.loads(changed["results"]["results"][0]["response"]["raw"])
            turn["items"] = [{"id": "unsafe-item", "type": item_type}]
            changed["results"]["results"][0]["response"]["raw"] = json.dumps(turn)
            with self.subTest(item_type=item_type):
                self.assert_rejected(changed, item_type)

    def test_parser_normalizes_command_items_without_persisting_secrets_or_raw_logs(self):
        secret = "synthetic-secret-value"
        command = {
            "id": "command-with",
            "type": "command_execution",
            "command": f"rg {secret} inputs",
            "aggregated_output": f"match: {secret}\n",
            "exit_code": 0,
            "status": "completed",
        }
        changed = self.document()
        raw = json.loads(changed["results"]["results"][0]["response"]["raw"])
        raw["items"].insert(0, command)
        changed["results"]["results"][0]["response"]["raw"] = json.dumps(raw)

        parsed = self.parse(changed, secrets=(secret,))
        event = next(
            event for event in parsed.arms[0].events
            if event["type"] == "tool_attempt"
        )
        serialized = json.dumps(parsed.to_payload(), sort_keys=True)

        self.assertEqual(event["tool"], "sandboxed_command")
        self.assertEqual(event["outcome"], "completed")
        self.assertNotIn("command", event)
        self.assertNotIn("aggregated_output", event)
        self.assertNotIn(secret, serialized)
        self.assertNotIn("rg [REDACTED] inputs", serialized)
        self.assertEqual(
            event["command_digest"],
            hashlib.sha256(b"rg [REDACTED] inputs").hexdigest(),
        )
        self.assertEqual(event["output_bytes"], len("match: [REDACTED]\n".encode()))

    def test_parser_rejects_malformed_incomplete_or_duplicate_command_items(self):
        base = {
            "id": "command-with",
            "type": "command_execution",
            "command": "pwd",
            "aggregated_output": "fixture\n",
            "exit_code": 0,
            "status": "completed",
        }
        malformed = []
        for field in ("id", "command", "aggregated_output", "exit_code", "status"):
            item = deepcopy(base)
            del item[field]
            malformed.append([item])
        mismatch = deepcopy(base)
        mismatch["exit_code"] = 9
        malformed.append([mismatch])
        in_progress = deepcopy(base)
        in_progress["status"] = "in_progress"
        malformed.append([in_progress])
        malformed.append([deepcopy(base), deepcopy(base)])

        for items in malformed:
            changed = self.document()
            turn = json.loads(changed["results"]["results"][0]["response"]["raw"])
            turn["items"] = items
            changed["results"]["results"][0]["response"]["raw"] = json.dumps(turn)
            with self.subTest(items=items):
                self.assert_rejected(changed)

    def test_parser_keeps_quality_grades_separate_from_safety_events(self):
        parsed = self.parse(self.document())
        arm = parsed.arms[0]
        events = json.dumps(arm.events, sort_keys=True)

        self.assertEqual(arm.quality["score"], 1.0)
        self.assertEqual(arm.quality["grading_result"]["reason"],
                         "quality grade for with_skill")
        self.assertNotIn("quality grade", events)
        self.assertNotIn("grading", events)
        self.assertNotIn("score", events)

    def test_parser_binds_each_normalized_trace_to_source_result_digest(self):
        document = self.document()
        parsed = self.parse(document)

        expected = {}
        for result in document["results"]["results"]:
            label = result["provider"]["label"]
            arm = label.replace("_", "-")
            expected[arm] = hashlib.sha256(
                json.dumps(
                    result, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                ).encode("utf-8")
            ).hexdigest()

        for arm in parsed.arms:
            self.assertEqual(arm.source_result_digest, expected[arm.arm_name])
            self.assertTrue(arm.events)
            self.assertTrue(all(
                event["source_result_digest"] == arm.source_result_digest
                for event in arm.events
            ))
            self.assertEqual(
                arm.provider_result["source_result_digest"], arm.source_result_digest
            )
            self.assertEqual(
                arm.provider_result_digest,
                hashlib.sha256(json.dumps(
                    arm.provider_result,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
