"""Mock-only regression tests for track-working-groups; no network calls."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from urllib.parse import urlsplit

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wg_runtime", PACKAGE / "scripts" / "wg.py")
wg = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wg)
NOW = datetime(2026, 11, 4, 15, 0, tzinfo=timezone.utc)
TIME = "2026-11-04T14:00:00Z"
SHA = "a" * 40


def fixture_get(url):
    path = urlsplit(url).path
    if path.endswith("/issues"):
        return [
            {"number": 7, "title": "Define accuracy and reliability", "state": "open",
             "updated_at": TIME},
            {"number": 8, "title": "Duplicate PR", "state": "open",
             "updated_at": TIME, "pull_request": {"url": "x"}}
        ]
    if path.endswith("/pulls"):
        return [{"number": 8, "title": "Add draft definitions", "state": "open",
                 "updated_at": TIME, "merged_at": None}]
    if path.endswith("/commits"):
        return [{"sha": SHA, "commit": {"message": "docs: update charter\n\nbody",
                                      "committer": {"date": TIME}}}]
    raise AssertionError("Unexpected URL: " + url)


class WorkingGroupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / "wg-data"
        with wg.locked(self.base):
            self.registry, self.state = wg.initialize(self.base)

    def call(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            wg.main(["--data-dir", str(self.base), *args])
        return buf.getvalue()

    def test_seed_has_five_stable_groups_without_membership_claims(self):
        self.assertEqual([g["id"] for g in self.registry["groups"]],
                         ["WG-0001", "WG-0002", "WG-0003", "WG-0004", "WG-0005"])
        self.assertTrue(all(g["membership_status"] == "unconfirmed"
                            for g in self.registry["groups"]))
        self.assertTrue(all(g["sources"] for g in self.registry["groups"]))
        self.assertEqual(wg.validate_registry(self.registry), self.registry)

    def test_add_edit_archive_resume_preserves_id_and_slug(self):
        self.assertIn("WG-0006", self.call("add", "--name", "New WG",
                                         "--github", "https://github.com/example/repo"))
        self.call("edit", "new-wg", "--name", "Renamed", "--membership", "observer",
                  "--priority", "high")
        self.assertIn("paused", self.call("pause", "WG-0006"))
        self.assertIn("archived", self.call("remove", "WG-0006", "--yes"))
        self.assertIn("active", self.call("resume", "WG-0006"))
        registry = wg.load_json(self.base / "groups.json")
        group = wg.select_group(registry, "new-wg")
        self.assertEqual((group["id"], group["slug"], group["name"], group["membership_status"]),
                         ("WG-0006", "new-wg", "Renamed", "observer"))

    def test_duplicate_ids_and_slugs_rejected(self):
        self.call("add", "--name", "Example WG")
        with self.assertRaises(wg.WGError):
            self.call("add", "--name", "Example WG")
        broken = copy.deepcopy(self.registry)
        broken["groups"][1]["id"] = "WG-0001"
        with self.assertRaises(wg.WGError):
            wg.validate_registry(broken)

    def test_default_refresh_sections_and_group_order(self):
        report = wg.run_update(copy.deepcopy(self.registry), copy.deepcopy(self.state),
                               NOW, getter=lambda url: [])
        self.assertEqual(report["summary"], {
            "groups_checked": 5, "new_or_changed": 0,
            "sources_ok": 5, "sources_unavailable": 0})
        self.assertEqual([g["id"] for g in report["groups"]],
                         ["WG-0001", "WG-0002", "WG-0003", "WG-0004", "WG-0005"])
        body = wg.render_briefing(report)
        headings = ["## 1. Overview", "## 2. Working Group Updates",
                    "## 3. Proposals & Decisions", "## 4. Upcoming Meetings",
                    "## 5. Learning Connections", "## 6. Sources & Checkpoint Status"]
        self.assertEqual([body.index(h) for h in headings],
                         sorted(body.index(h) for h in headings))
        self.assertIn("No new or changed items", body)
        self.assertIn("No verified upcoming meetings", body)

    def test_fingerprints_and_replays_are_idempotent(self):
        report1 = wg.run_update(self.registry, self.state, NOW,
                                group_id="WG-0001", getter=fixture_get)
        self.assertEqual(report1["summary"]["new_or_changed"], 3)
        updates = report1["groups"][0]["updates"]
        self.assertEqual(set(e["kind"] for e in updates),
                         {"issue", "pull_request", "commit"})
        before = sorted(e["id"] for e in updates)
        self.assertTrue(all(x.startswith("UPD-") for x in before))
        report2 = wg.run_update(self.registry, self.state, NOW,
                                group_id="WG-0001", getter=fixture_get)
        self.assertEqual(report2["summary"]["new_or_changed"], 0)
        repo = "github:aaif/wg-accuracy-and-reliability"
        self.assertEqual(sorted(self.state["groups"]["WG-0001"]["sources"][repo]["seen"]),
                         before)

    def test_changed_event_keeps_the_same_id(self):
        first = wg.run_update(self.registry, self.state, NOW,
                              group_id="WG-0001", getter=fixture_get)
        by_url = {e["url"]: e["id"] for e in first["groups"][0]["updates"]}
        def changed(url):
            events = fixture_get(url)
            if urlsplit(url).path.endswith("/issues"):
                events[0] = dict(events[0], title="Revised issue title")
            return events
        second = wg.run_update(self.registry, self.state, NOW,
                               group_id="WG-0001", getter=changed)
        self.assertEqual(len(second["groups"][0]["updates"]), 1)
        event = second["groups"][0]["updates"][0]
        self.assertEqual(event["id"], by_url[event["url"]])

    def test_failed_fetch_does_not_advance_a_source(self):
        wg.run_update(self.registry, self.state, NOW,
                      group_id="WG-0001", getter=fixture_get)
        key = "github:aaif/wg-accuracy-and-reliability"
        before = copy.deepcopy(self.state["groups"]["WG-0001"]["sources"][key])
        def unavailable(url):
            raise wg.WGError("synthetic outage")
        report = wg.run_update(self.registry, self.state, NOW.replace(hour=16),
                               group_id="WG-0001", getter=unavailable)
        after = self.state["groups"]["WG-0001"]["sources"][key]
        self.assertEqual(after["checked_at"], before["checked_at"])
        self.assertEqual(after["seen"], before["seen"])
        self.assertEqual(after["last_error"], "synthetic outage")
        self.assertEqual(report["summary"]["sources_unavailable"], 1)
        self.assertIn("unavailable", wg.render_briefing(report))

    def test_partial_failure_allows_other_sources_to_succeed(self):
        def some_fail(url):
            if "wg-identity-and-trust" in url:
                raise wg.WGError("temporary")
            return []
        report = wg.run_update(self.registry, self.state, NOW, getter=some_fail)
        self.assertEqual((report["summary"]["sources_ok"],
                          report["summary"]["sources_unavailable"]), (4, 1))
        self.assertIsNone(self.state["groups"]["WG-0002"]["sources"][
            "github:aaif/wg-identity-and-trust"].get("checked_at"))
        self.assertEqual(self.state["groups"]["WG-0001"]["sources"][
            "github:aaif/wg-accuracy-and-reliability"]["checked_at"], wg.iso(NOW))

    def test_pagination_overflow_fails_closed(self):
        def too_many(url):
            return [{"updated_at": TIME} for _ in range(wg.PAGE_SIZE)]
        with self.assertRaisesRegex(wg.WGError, "pagination"):
            wg.github_pages("aaif/repo", "pulls", {}, NOW.replace(hour=13),
                            getter=too_many, stop_on_old=True)

    def test_report_persistence_and_archived_runs(self):
        report = wg.run_update(self.registry, self.state, NOW,
                               group_id="WG-0001", getter=fixture_get)
        saved = wg.store_report(self.base, report, self.state)
        self.assertTrue(saved.is_file())
        self.assertEqual(wg.load_json(self.base / "reports" / "latest.json")[
            "summary"]["new_or_changed"], 3)
        self.assertIn("## 6. Sources & Checkpoint Status",
                      (self.base / "reports" / "latest.md").read_text())
        wg.validate_state(wg.load_json(self.base / "state.json"))
        replay_path = wg.store_report(self.base, report, self.state)
        self.assertNotEqual(saved, replay_path)

    def test_note_key_is_stable_and_overwrites_are_gated(self):
        group = self.registry["groups"][0]
        src = self.base / "meeting.txt"
        src.write_text("First note")
        args = SimpleNamespace(file=str(src), key="meeting-2026-11-04",
                               title="WG notes", source_url=None, replace=False)
        ident, status = wg.import_note(self.base, group, args)
        self.assertTrue(ident.startswith("DOC-"))
        self.assertEqual(status, "saved")
        self.assertEqual(wg.import_note(self.base, group, args), (ident, "unchanged"))
        src.write_text("Revised note")
        with self.assertRaisesRegex(wg.WGError, "replace"):
            wg.import_note(self.base, group, args)
        args.replace = True
        self.assertEqual(wg.import_note(self.base, group, args), (ident, "saved"))

    def test_reset_preserves_registry_and_notes(self):
        group = self.registry["groups"][0]
        _, path = wg.note_file(self.base, group, "test")
        wg.atomic_text(path, "Private record")
        self.state["groups"]["WG-0001"] = {"sources": {}}
        wg.save_state(self.base, self.state)
        self.call("reset", "WG-0001", "--yes")
        self.assertFalse(wg.load_json(self.base / "state.json")["groups"])
        self.assertEqual(len(wg.load_json(self.base / "groups.json")["groups"]), 5)
        self.assertEqual(path.read_text(), "Private record")

    def test_membership_meeting_and_timezone(self):
        self.call("edit", "WG-0002", "--membership", "observer")
        output = self.call("meeting", "add", "WG-0002", "--when",
                           "2026-11-10T09:00:00-08:00",
                           "--title", "Example meeting",
                           "--url", "https://aaif.io/working-groups")
        self.assertTrue(output.strip().startswith("MTG-"))
        self.assertIn("Example meeting", self.call("meeting", "list", "WG-0002"))
        group = wg.select_group(wg.load_json(self.base / "groups.json"), "WG-0002")
        self.assertEqual(group["meetings"][0]["starts_at"], "2026-11-10T17:00:00Z")
        self.assertEqual(group["membership_status"], "observer")

    def test_invalid_source_urls_and_unsafe_paths_are_rejected(self):
        for url in ("http://github.com/a/b", "https://github.com/a/b/issues/1",
                    "https://github.com/secret@evil.test/a/b", "file:///etc/passwd"):
            with self.assertRaises(wg.WGError):
                wg.github_repo(url)
        with self.assertRaises(wg.WGError):
            wg.note_file(self.base, self.registry["groups"][0], "../escape")
        with self.assertRaises(wg.WGError):
            with wg.locked(PACKAGE):
                pass

    def test_notes_root_symlink_is_rejected(self):
        target = self.base / "elsewhere"
        target.mkdir()
        (self.base / "notes").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(wg.WGError, "symlink"):
            wg.note_file(self.base, self.registry["groups"][0], "meeting-2026-11-04")

    def test_malformed_github_item_fails_source_without_checkpoint(self):
        def malformed(url):
            if urlsplit(url).path.endswith("/issues"):
                return [{"title": "No issue number", "updated_at": TIME}]
            return []
        report = wg.run_update(self.registry, self.state, NOW,
                               group_id="WG-0001", getter=malformed)
        self.assertEqual(report["summary"]["sources_unavailable"], 1)
        source = self.state["groups"]["WG-0001"]["sources"][
            "github:aaif/wg-accuracy-and-reliability"]
        self.assertIsNone(source.get("checked_at"))
        self.assertEqual(source.get("seen"), {})


    def aaif_fixture(self):
        """Synthetic Flight stream with public event metadata and a private-looking join URL."""
        entries = [
            ("99263049290:2026-11-05T17:00:00Z", "Identity & Trust Working Group",
             "identity-trust", "2026-11-05T17:00:00Z"),
            ("96669513178:2026-11-05T18:00:00Z",
             "Governance, Risk & Regulatory Alignment Working Group",
             "governance-risk-regulatory-alignment", "2026-11-05T18:00:00Z"),
            ("96916295650:2026-11-05T18:00:00Z",
             "Observability & Tracing - Agent State, Context, and Reasoning",
             "observability-traceability", "2026-11-05T18:00:00Z"),
        ]
        data = [{"_id": eid, "_type": "event", "title": title,
                 "startsAt": starts, "endsAt": None,
                 "joinUrl": "https://zoom-lfx.platform.linuxfoundation.org/meeting/123?password=SECRETPASS",
                 "meeting": {"meetingId": eid.split(":")[0], "groupSlug": group,
                             "durationMinutes": 60}}
                for eid, title, group, starts in entries]
        return "<html><script>self.__next_f.push([1," + json.dumps(
            "a0:" + json.dumps(data)) + "])</script></html>"

    def test_public_calendar_parses_three_source_events_with_stable_ids(self):
        html = self.aaif_fixture()
        entries = wg.parse_aaif_calendar(html, NOW, days=14)
        again = wg.parse_aaif_calendar(html, NOW, days=14)
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries, again)
        self.assertEqual({e["group_slug"] for e in entries},
                         {"identity-trust", "observability-traceability",
                          "governance-risk-regulatory-alignment"})
        self.assertTrue(all(e["id"].startswith("MTG-") for e in entries))
        self.assertEqual(len({e["id"] for e in entries}), 3)
        self.assertTrue(all(e["source"] == "aaif_public_calendar" for e in entries))

    def test_public_calendar_drops_sensitive_join_data(self):
        html = self.aaif_fixture()
        parsed = wg.parse_aaif_calendar(html, NOW)
        self.assertIn("SECRETPASS", html)
        self.assertNotIn("SECRETPASS", json.dumps(parsed))
        self.assertNotIn("zoom-lfx", json.dumps(parsed))
        self.assertTrue(all(e["url"].startswith("https://aaif.io/working-groups/") for e in parsed))

    def test_calendar_meeting_match_untracked_and_pacific_time(self):
        entries = wg.parse_aaif_calendar(self.aaif_fixture(), NOW)
        report = wg.run_update(self.registry, self.state, NOW, getter=lambda url: [],
                               calendar_events=entries)
        self.assertEqual(report["calendar"]["status"], "ok")
        self.assertEqual(report["calendar"]["new_or_changed"], 3)
        self.assertEqual(len(report["calendar"]["untracked_meetings"]), 1)
        self.assertEqual(report["calendar"]["untracked_meetings"][0]["group_slug"],
                         "governance-risk-regulatory-alignment")
        by_group = {g["id"]: g for g in report["groups"]}
        self.assertEqual(len(by_group["WG-0002"]["meetings"]), 1)
        self.assertEqual(len(by_group["WG-0004"]["meetings"]), 1)
        self.assertEqual(len(by_group["WG-0001"]["meetings"]), 0)
        self.assertIn("09:00 AM PST", wg.render_briefing(report))
        self.assertIn("10:00 AM PST", wg.render_briefing(report))
        self.assertIn("Other AAIF meetings", wg.render_briefing(report))
        self.assertNotIn("SECRETPASS", json.dumps(report))
        self.assertEqual(len(self.registry["groups"]), 5)  # Do not add governance as member.

    def test_calendar_checkpoint_replay_and_error_isolation(self):
        entries = wg.parse_aaif_calendar(self.aaif_fixture(), NOW)
        first = wg.run_update(self.registry, self.state, NOW, getter=lambda url: [],
                              calendar_events=entries)
        self.assertEqual(first["calendar"]["new_or_changed"], 3)
        before = copy.deepcopy(self.state["calendar"])
        second = wg.run_update(self.registry, self.state, NOW, getter=lambda url: [],
                               calendar_events=entries)
        self.assertEqual(second["calendar"]["new_or_changed"], 0)
        failed = wg.run_update(self.registry, self.state, NOW.replace(hour=16),
                               getter=lambda url: [], calendar_error="Synthetic outage")
        self.assertEqual(failed["calendar"]["status"], "unavailable")
        self.assertEqual(self.state["calendar"]["checked_at"], before["checked_at"])
        self.assertEqual(self.state["calendar"]["seen"], before["seen"])
        self.assertEqual(failed["summary"]["sources_ok"], 5)
        self.assertNotIn("No verified upcoming meetings in the local registry",
                         wg.render_briefing(failed))
        self.assertIn("NOT evidence", wg.render_briefing(failed))
        wg.validate_state(self.state)
        wg.store_report(self.base, failed, self.state)
        self.assertEqual(wg.load_json(self.base / "state.json")["calendar"]["checked_at"],
                         before["checked_at"])

    def test_bare_wg_command_auto_fetches_and_persists_calendar(self):
        with mock.patch.object(wg, "fetch_aaif_calendar", return_value=self.aaif_fixture()), \
             mock.patch.object(wg, "github_events", return_value=[]):
            result = self.call()
        self.assertIn("Public AAIF calendar: ok", result)
        self.assertIn("Other AAIF meetings", result)
        self.assertEqual(wg.load_json(self.base / "reports" / "latest.json")
                         ["calendar"]["status"], "ok")
        self.assertEqual(len(wg.load_json(self.base / "state.json")
                             ["calendar"]["seen"]), 3)

    def test_first_calendar_outage_keeps_valid_empty_checkpoint(self):
        report = wg.run_update(self.registry, self.state, NOW,
                               update_github=False, calendar_error="Synthetic outage")
        self.assertEqual(self.state["calendar"], {
            "checked_at": None, "last_error": "Synthetic outage", "seen": {}})
        wg.validate_state(self.state)
        self.assertEqual(report["calendar"]["status"], "unavailable")
        self.assertIn("NOT evidence", wg.render_briefing(report))

    def test_calendar_only_skips_github_without_changing_github_state(self):
        entries = wg.parse_aaif_calendar(self.aaif_fixture(), NOW)
        report = wg.run_update(self.registry, self.state, NOW,
                               update_github=False, calendar_events=entries)
        self.assertEqual(report["summary"]["sources_ok"], 0)
        self.assertTrue(all(g["sources"][0]["status"] == "not_checked"
                            for g in report["groups"]))
        self.assertIn("GitHub updates were not checked", wg.render_briefing(report))
        self.assertEqual(self.state["groups"]["WG-0002"]["sources"], {})
        self.assertEqual(len(report["calendar"]["untracked_meetings"]), 1)

    def test_public_meetings_override_manual_same_start_and_title(self):
        entries = wg.parse_aaif_calendar(self.aaif_fixture(), NOW)
        group = wg.select_group(self.registry, "WG-0002")
        group["meetings"].append({
            "id": wg.stable_id("MTG", "manual-demo"),
            "title": "Identity & Trust Working Group",
            "starts_at": "2026-11-05T17:00:00Z",
            "url": None})
        report = wg.run_update(self.registry, self.state, NOW,
                               getter=lambda url: [], calendar_events=entries)
        group_report = next(g for g in report["groups"] if g["id"] == "WG-0002")
        self.assertEqual(len(group_report["meetings"]), 1)
        self.assertEqual(group_report["meetings"][0]["source"], "aaif_public_calendar")

    def test_calendar_safety_rejects_wrong_format_dates_and_windows(self):
        with self.assertRaisesRegex(wg.WGError, "readable event payload"):
            wg.parse_aaif_calendar("<html>No Flight data</html>", NOW)
        with self.assertRaisesRegex(wg.WGError, "1–90"):
            wg.parse_aaif_calendar(self.aaif_fixture(), NOW, days=91)
        self.assertEqual(wg.parse_aaif_calendar(self.aaif_fixture(),
                                                NOW + wg.timedelta(days=40)), [])
        self.assertIn("10:00 AM PDT",
                      wg.format_pacific("2026-10-15T17:00:00Z"))

    def test_cancelled_event_is_not_reported(self):
        event = {"_id": "aaa:2026-11-05T18:00:00Z", "_type": "event",
                 "title": "Cancelled meeting", "startsAt": "2026-11-05T18:00:00Z",
                 "isCancelled": True,
                 "meeting": {"groupSlug": "identity-trust", "durationMinutes": 60}}
        html = '<script>self.__next_f.push([1,' + json.dumps(
            "a0:" + json.dumps([event])) + '])</script>'
        self.assertEqual(wg.parse_aaif_calendar(html, NOW), [])

    def test_calendar_schema_extensions_and_old_state_compatibility(self):
        state_schema = json.loads((PACKAGE / "schemas" / "state.schema.json").read_text())
        report_schema = json.loads((PACKAGE / "schemas" / "briefing.schema.json").read_text())
        self.assertIn("calendar", state_schema["properties"])
        self.assertIn("calendar", report_schema["properties"])
        self.assertIn("source", report_schema["properties"]["groups"]["items"]
                      ["properties"]["meetings"]["items"]["properties"])
        self.assertEqual(wg.validate_state({"schema_version": 1, "groups": {}}),
                         {"schema_version": 1, "groups": {}})

    def test_confirmation_flags_are_required(self):
        with self.assertRaises(wg.WGError):
            self.call("remove", "WG-0001")
        with self.assertRaises(wg.WGError):
            self.call("reset")
        with self.assertRaises(wg.WGError):
            self.call("meeting", "remove", "WG-0001", "MTG-INVALID")

    def test_lookback_override_cannot_truncate_checkpoint_window(self):
        self.state["groups"]["WG-0001"] = {"sources": {
            "github:aaif/wg-accuracy-and-reliability": {
                "seen": {}, "checked_at": "2026-10-10T15:00:00Z"}}}
        urls = []
        def capture(url):
            urls.append(url)
            return []
        wg.run_update(self.registry, self.state, NOW,
                      group_id="WG-0001", since_override=wg.duration("1d"),
                      getter=capture)
        self.assertTrue(any("2026-10-09" in url for url in urls))
        self.assertEqual(wg.duration("2w").days, 14)

    def test_contract_schemas_and_template_are_present(self):
        for name in ("groups", "state", "briefing"):
            schema = json.loads((PACKAGE / "schemas" /
                                 (name + ".schema.json")).read_text())
            self.assertEqual(schema["$schema"],
                             "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["properties"]["schema_version"]["const"], 1)
        template = (PACKAGE / "templates" / "briefing.md").read_text()
        for num, name in enumerate(("Overview", "Working Group Updates",
                                    "Proposals & Decisions", "Upcoming Meetings",
                                    "Learning Connections",
                                    "Sources & Checkpoint Status"), 1):
            self.assertIn("## " + str(num) + ". " + name, template)


if __name__ == "__main__":
    unittest.main()
