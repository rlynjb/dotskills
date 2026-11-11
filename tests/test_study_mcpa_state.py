"""Isolated functional tests: no writes to a learner's real progress location."""
from __future__ import annotations

from contextlib import redirect_stdout
from datetime import date
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "study-mcpa" / "scripts" / "study_state.py"
spec = importlib.util.spec_from_file_location("study_state", SCRIPT)
assert spec and spec.loader
study_state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study_state)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "private" / "progress.json"

    def call(self, command, *args, expect=0):
        out = io.StringIO()
        with redirect_stdout(out):
            code = study_state.main(["--state", str(self.path), command, *args])
        result = json.loads(out.getvalue())
        self.assertEqual(code, expect, result)
        return result

    def init(self):
        self.call("init", "--approve")

    def select(self, item="F-01", rev=0, mode=None):
        args = ["--id", item, "--expected-revision", str(rev)]
        if mode:
            args.extend(["--mode", mode])
        return self.call("select", *args)

    def test_one_time_opt_in_and_permissions(self):
        self.call("init", expect=1)
        self.assertFalse(self.path.exists())
        self.init()
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.path.parent.stat().st_mode & 0o777, 0o700)
        self.call("init", "--approve", expect=1)

    def test_status_resume_are_read_only(self):
        self.init()
        original = self.path.read_bytes()
        self.assertEqual(self.call("status")["revision"], 0)
        self.assertEqual(self.call("resume")["revision"], 0)
        self.assertEqual(self.path.read_bytes(), original)

    def test_unknown_id_and_stale_revision_fail_closed(self):
        self.init()
        self.call("select", "--id", "F-99", "--expected-revision", "0", expect=1)
        self.assertEqual(self.call("status")["revision"], 0)
        self.select()
        self.call("select", "--id", "A-01", "--expected-revision", "0", expect=1)
        self.assertEqual(self.call("status")["active"]["item_id"], "F-01")

    def test_pending_checkpoint_and_switch_restore(self):
        self.init()
        self.select()
        self.call("checkpoint", "--step", "teach-back", "--next-action", "Answer F-01 teach-back", "--expected-revision", "1")
        self.select("A-01", 2)
        resume = self.select("F-01", 3)
        self.assertEqual(resume["active"]["checkpoint_id"], "teach-back")
        self.assertEqual(resume["active"]["next_action"], "Answer F-01 teach-back")
        self.assertIn("A-01", self.call("status")["progress"]["topics"])

    def test_manual_partial_checkpoint_does_not_claim_completion(self):
        self.init()
        self.select()
        self.call("checkpoint", "--expected-revision", "1", "--note", "Need another example")
        item = self.call("status")["progress"]["topics"]["F-01"]
        self.assertEqual(item["status"], "learning")
        self.assertEqual(item["completed_checkpoints"], [])
        self.assertEqual(item["cursor"]["resume_note"], "Need another example")

    def test_checkpoint_completion_requires_evidence(self):
        self.init()
        self.select()
        self.call("checkpoint", "--step", "teach-back", "--outcome", "completed", "--expected-revision", "1", expect=1)
        complete = self.call("checkpoint", "--step", "teach-back", "--outcome", "completed", "--evidence", "Explained MCP role boundaries correctly", "--expected-revision", "1")
        self.assertEqual(complete["active"]["checkpoint_id"], "ready")
        item = self.call("status")["progress"]["topics"]["F-01"]
        self.assertIn("teach-back", item["completed_checkpoints"])
        self.assertNotEqual(item["status"], "confident")

    def test_practice_results_idempotent_and_review_queue(self):
        self.init()
        self.select(mode="Practice")
        params = ["--kind", "Practice", "--id", "F-01", "--attempted", "1", "--correct", "0", "--confidence", "high", "--evidence", "Answered A, correct was B", "--misconception", "Confused client/server", "--on-date", "2026-11-03", "--event-id", "q1", "--expected-revision", "1"]
        result = self.call("record", *params)
        self.assertTrue(result["saved"])
        repeated = self.call("record", *params)
        self.assertFalse(repeated["saved"])
        self.assertEqual(repeated["revision"], 2)
        progress = self.call("status")["progress"]
        self.assertEqual(len(progress["assessments"]), 1)
        self.assertEqual(progress["topics"]["F-01"]["status"], "needs review")
        self.assertEqual(progress["review_queue"][0]["due_date"], "2026-11-03")
        self.assertEqual(len(self.call("review", "--on-date", "2026-11-03")["due_topics"]), 1)
        self.select(mode="Review", rev=2)
        self.call("record", "--kind", "Review", "--id", "F-01", "--attempted", "1", "--correct", "1", "--confidence", "high", "--evidence", "Correctly explained client/server roles", "--on-date", "2026-11-04", "--event-id", "r1", "--expected-revision", "3")
        self.assertEqual(self.call("status")["progress"]["review_queue"][0]["due_date"], "2026-11-07")
        self.call("record", "--kind", "Review", "--id", "F-01", "--attempted", "1", "--correct", "1", "--evidence", "Applied role distinction", "--on-date", "2026-11-07", "--event-id", "r2", "--expected-revision", "4")
        self.assertEqual(self.call("status")["progress"]["review_queue"][0]["due_date"], "2026-11-14")
        self.call("record", "--kind", "Review", "--id", "F-01", "--attempted", "1", "--correct", "1", "--evidence", "Correct recall", "--on-date", "2026-11-14", "--event-id", "r3", "--expected-revision", "5")
        self.assertEqual(self.call("status")["progress"]["review_queue"], [])

    def test_record_requires_matching_mode_and_event_id(self):
        self.init()
        self.select()  # Guided
        args = ["--kind", "Practice", "--id", "F-01", "--attempted", "1", "--correct", "1", "--evidence", "Answered", "--expected-revision", "1"]
        self.call("record", *args, expect=1)
        self.call("record", *args, "--event-id", "q2", expect=1)
        self.assertEqual(self.call("status")["revision"], 1)

    def test_lab_verified_vs_proposed_and_approval(self):
        self.init()
        self.select("L-01")
        self.call("lab", "--step", "step-1", "--kind", "proposed", "--evidence", "Review catalog", "--verified", "--event-id", "l1", "--expected-revision", "1", expect=1)
        self.call("lab", "--step", "step-1", "--kind", "actually_run", "--evidence", "Ran inspection", "--verified", "--event-id", "l1", "--expected-revision", "1", expect=1)
        valid = self.call("lab", "--step", "step-1", "--kind", "inspected", "--evidence", "Observed catalog names", "--verified", "--event-id", "l1", "--expected-revision", "1")
        self.assertEqual(valid["active"]["checkpoint_id"], "step-2")
        self.assertEqual(self.call("status")["progress"]["labs"]["L-01"]["status"], "learning")

    def test_mock_interruption_and_submitted_only(self):
        self.init()
        self.call("mock-start", "--length", "20", "--expected-revision", "0")
        resumed = self.call("resume")
        self.assertIn("interrupted", resumed["warning"])
        self.assertNotIn("answer", json.dumps(resumed["progress"]["mock"]).lower())
        self.call("record", "--kind", "Mock", "--attempted", "17", "--correct", "14", "--evidence", "Scored 17 submitted answers", "--event-id", "mock-1", "--expected-revision", "1")
        self.assertEqual(self.call("status")["progress"]["mock"]["status"], "submitted")

    def test_stopping_interrupted_mock_preserves_topics(self):
        self.init()
        self.select()
        self.call("mock-start", "--length", "10", "--expected-revision", "1")
        self.call("mock-stop", "--expected-revision", "2", expect=1)
        self.call("mock-stop", "--confirm-stop", "--expected-revision", "2")
        status = self.call("status")
        self.assertEqual(status["progress"]["mock"]["status"], "interrupted")
        self.assertIn("F-01", status["progress"]["topics"])
        self.call("mock-start", "--length", "20", "--expected-revision", "3")

    def test_corruption_and_version_mismatch_do_not_overwrite(self):
        self.init()
        self.select()
        state = json.loads(self.path.read_text())
        state["curriculum_version"] = 900
        self.path.write_text(json.dumps(state))
        existing = self.path.read_bytes()
        self.call("checkpoint", "--expected-revision", "1", expect=1)
        self.assertEqual(self.path.read_bytes(), existing)
        self.path.write_text("broken json")
        self.call("status", expect=1)
        self.assertEqual(self.path.read_bytes(), b"broken json")
        self.assertTrue(self.path.with_name("progress.json.bak").exists())

    def test_reset_and_correction_are_approved_and_backed_up(self):
        self.init()
        self.select()
        self.call("correct", "--id", "F-01", "--status", "confident", "--reason", "Confirmed recall on two occasions", "--expected-revision", "1", expect=1)
        self.call("correct", "--id", "F-01", "--status", "confident", "--reason", "Confirmed recall on two occasions", "--confirm-correction", "--expected-revision", "1")
        self.assertEqual(self.call("status")["progress"]["topics"]["F-01"]["status"], "confident")
        self.call("reset", "--expected-revision", "2", expect=1)
        self.call("reset", "--confirm-reset", "--expected-revision", "2")
        self.assertEqual(self.call("status")["revision"], 3)
        self.assertEqual(self.call("status")["progress"]["topics"], {})
        backup = json.loads(self.path.with_name("progress.json.bak").read_text())
        self.assertEqual(backup["topics"]["F-01"]["status"], "confident")

    def test_state_path_cannot_be_under_installed_skill(self):
        with self.assertRaises(study_state.StateError):
            study_state.state_path(str(SCRIPT.parent / "progress.json"))

    def test_catalog_covers_all_existing_stable_ids(self):
        version, topics, labs = study_state.catalog()
        self.assertEqual(version, 1)
        self.assertEqual(len(topics), 17)
        self.assertEqual(len(labs), 5)
        self.assertIn("S-04", topics)
        self.assertEqual(labs["L-02"], 5)


if __name__ == "__main__":
    unittest.main()
