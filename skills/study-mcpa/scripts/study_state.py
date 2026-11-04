#!/usr/bin/env python3
"""Private, deterministic Study MCPA progress store. Python standard library only.

The harness chooses when to call this script. It cannot independently observe
chat checkpoints or guarantee persistence in clients without filesystem tools.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
CURRICULUM = SKILL_DIR / "references" / "curriculum.md"
LABS = SKILL_DIR / "references" / "dotskills-mcp-lab.md"
SCHEMA_VERSION = 1
TOPIC_STATUS = {"not started", "learning", "needs review", "confident"}
MODES = {"Guided", "Practice", "Review", "Lab", "Mock"}
STEPS = {
    "Guided": ("problem-scope", "high-level-map", "deep-dive", "teach-back", "ready"),
    "Practice": ("question", "feedback", "ready"),
    "Review": ("recall", "feedback", "ready"),
}
EVIDENCE_KINDS = {"proposed", "inspected", "actually_run"}


class StateError(Exception):
    """Known invalid state, command, or persistence condition."""


def today() -> date:
    return datetime.now(timezone.utc).date()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def short(value: str | None, label: str, length: int = 250) -> str | None:
    if value is not None and (not isinstance(value, str) or len(value) > length or "\x00" in value):
        raise StateError(f"{label} must be at most {length} characters without NUL")
    return value


def catalog() -> tuple[int, set[str], dict[str, int]]:
    try:
        curriculum = CURRICULUM.read_text(encoding="utf-8")
        lab_text = LABS.read_text(encoding="utf-8")
    except OSError as exc:
        raise StateError(f"Cannot load installed curriculum: {exc}") from exc
    match = re.search(r"^<!-- curriculum_version: (\d+) -->$", curriculum, re.M)
    if not match:
        raise StateError("Curriculum has no explicit version; cannot safely resume")
    topics = re.findall(r"^- \*\*([FAISE]-\d{2})\*\* — ", curriculum, re.M)
    blocks = re.split(r"(?=^### L-\d{2} — )", lab_text, flags=re.M)
    labs: dict[str, int] = {}
    for block in blocks:
        item = re.match(r"### (L-\d{2}) — ", block)
        if item:
            labs[item.group(1)] = len(re.findall(r"^\d+\. ", block, re.M))
    if len(topics) != 17 or len(set(topics)) != 17 or len(labs) != 5 or any(n < 1 for n in labs.values()):
        raise StateError("Expected 17 unique study topics and five numbered labs; review curriculum changes")
    return int(match.group(1)), set(topics), labs


def state_path(cli_value: str | None) -> Path:
    raw = cli_value or os.environ.get("STUDY_MCPA_STATE_PATH") or "~/.dotskills/study-mcpa/progress.json"
    path = Path(raw).expanduser().resolve()
    if path.is_relative_to(SKILL_DIR.resolve()):
        raise StateError("Personal progress must live outside the installed Study MCPA skill")
    if path.suffix != ".json" or path.name.startswith("."):
        raise StateError("The state path must name a JSON file")
    return path


def initial(version: int) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "curriculum_version": version,
        "revision": 0,
        "created_at": now,
        "last_saved_at": now,
        "active": {"item_id": None, "mode": None, "checkpoint_id": None, "next_action": None, "resume_note": None},
        "topics": {}, "labs": {}, "assessments": [], "review_queue": [],
        "mock": None, "applied_event_ids": [],
    }


def valid_step(item_id: str, mode: str, step: str, labs: dict[str, int]) -> bool:
    if not isinstance(step, str):
        return False
    if mode == "Lab" and item_id in labs:
        return step == "ready" or step in {f"step-{n}" for n in range(1, labs[item_id] + 1)}
    if mode == "Mock":
        return step in {"mock-in-progress", "ready"}
    return step in STEPS.get(mode, ())


def validate(state: Any, version: int, topics: set[str], labs: dict[str, int]) -> None:
    if not isinstance(state, dict) or state.get("schema_version") != SCHEMA_VERSION:
        raise StateError("Unknown state schema; no write performed (migration required)")
    if state.get("curriculum_version") != version:
        raise StateError("Curriculum version mismatch; no write performed (migration required)")
    if type(state.get("revision")) is not int or state["revision"] < 0:
        raise StateError("Invalid revision")
    for name in ("created_at", "last_saved_at"):
        if not isinstance(state.get(name), str):
            raise StateError(f"Missing {name}")
    for name in ("topics", "labs"):
        if not isinstance(state.get(name), dict):
            raise StateError(f"Invalid {name} map")
    if not isinstance(state.get("assessments"), list) or not isinstance(state.get("review_queue"), list):
        raise StateError("Invalid assessments or review queue")
    if not isinstance(state.get("applied_event_ids"), list) or any(not isinstance(x, str) or len(x) > 100 for x in state["applied_event_ids"]):
        raise StateError("Invalid event IDs")
    if len(state["applied_event_ids"]) > 200:
        raise StateError("Event history exceeds limit")
    for item_id, record in state["topics"].items():
        if item_id not in topics or not isinstance(record, dict) or record.get("status") not in TOPIC_STATUS:
            raise StateError(f"Invalid topic progress: {item_id}")
        check_cursor(record.get("cursor"), item_id, labs)
        if not isinstance(record.get("completed_checkpoints"), list):
            raise StateError(f"Invalid completed checkpoints: {item_id}")
        if not isinstance(record.get("misconceptions"), list) or any(not isinstance(v, str) or len(v) > 280 for v in record["misconceptions"]):
            raise StateError(f"Invalid misconception entries: {item_id}")
    for item_id, record in state["labs"].items():
        if item_id not in labs or not isinstance(record, dict):
            raise StateError(f"Invalid lab progress: {item_id}")
        check_cursor(record.get("cursor"), item_id, labs)
        if record.get("status") not in {"learning", "completed"}:
            raise StateError(f"Invalid lab status: {item_id}")
        if not isinstance(record.get("steps"), dict):
            raise StateError(f"Invalid lab steps: {item_id}")
        for step, result in record["steps"].items():
            if not valid_step(item_id, "Lab", step, labs) or step == "ready" or not isinstance(result, dict) or result.get("kind") not in EVIDENCE_KINDS or not isinstance(result.get("verified"), bool):
                raise StateError(f"Invalid lab evidence: {item_id}/{step}")
            short(result.get("evidence"), "lab evidence", 500)
            if result["verified"] and result["kind"] == "proposed":
                raise StateError("Proposed work cannot be verified as done")
    active = state.get("active")
    if not isinstance(active, dict):
        raise StateError("Invalid active cursor")
    item_id = active.get("item_id")
    if item_id is not None and item_id not in topics and item_id not in labs:
        raise StateError(f"Unknown active item: {item_id}")
    if item_id is not None:
        check_cursor(active, item_id, labs)
    elif active.get("mode") == "Mock":
        if active.get("checkpoint_id") not in {"mock-in-progress", "ready"}:
            raise StateError("Invalid mock checkpoint")
    elif any(active.get(k) is not None for k in ("mode", "checkpoint_id", "next_action", "resume_note")):
        raise StateError("Invalid empty cursor")
    if item_id is not None:
        entry = state["labs"].get(item_id) if item_id in labs else state["topics"].get(item_id)
        if entry is None or active != {"item_id": item_id, **entry["cursor"]}:
            raise StateError("Active cursor does not match saved item checkpoint")
    if state.get("mock") is not None:
        mock = state["mock"]
        if not isinstance(mock, dict) or mock.get("status") not in {"in_progress", "submitted", "interrupted"} or mock.get("length") not in {10, 20, 40}:
            raise StateError("Invalid mock progress")
    for item in state["review_queue"]:
        if not isinstance(item, dict) or item.get("item_id") not in topics or item.get("stage") not in {0, 1, 2}:
            raise StateError("Invalid review queue item")
        try:
            date.fromisoformat(item["due_date"])
        except (KeyError, TypeError, ValueError) as exc:
            raise StateError("Invalid review date") from exc


def check_cursor(cursor: Any, item_id: str, labs: dict[str, int]) -> None:
    if not isinstance(cursor, dict):
        raise StateError(f"Invalid cursor for {item_id}")
    mode = cursor.get("mode")
    if mode not in MODES or (item_id in labs) != (mode == "Lab") or not valid_step(item_id, mode, cursor.get("checkpoint_id"), labs):
        raise StateError(f"Invalid mode or step for {item_id}")
    short(cursor.get("next_action"), "next action")
    short(cursor.get("resume_note"), "resume note")


def read(path: Path, version: int, topics: set[str], labs: dict[str, int]) -> dict[str, Any]:
    if not path.is_file():
        raise StateError("No persistent state found. Ask for permission before running init --approve")
    if path.stat().st_size > 2_000_000:
        raise StateError("Progress file is unexpectedly large; inspect it before loading")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise StateError(f"Cannot read progress file; no changes made: {exc}") from exc
    validate(raw, version, topics, labs)
    return raw


@contextmanager
def write_lock(path: Path):
    lock_path = path.with_name(path.name + ".lock")
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise StateError("Progress file is locked by another writer; retry after checking that session") from exc
    try:
        os.close(fd)
        yield
    finally:
        lock_path.unlink(missing_ok=True)


def atomic_bytes(path: Path, payload: bytes) -> None:
    name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".study-state-", delete=False) as tmp:
            name = tmp.name
            os.chmod(name, 0o600)
            tmp.write(payload)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def serialize(state: dict[str, Any]) -> bytes:
    return (json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def transact(path: Path, version: int, topics: set[str], labs: dict[str, int], args: argparse.Namespace, mutate) -> tuple[dict[str, Any], bool]:
    if not path.parent.is_dir():
        raise StateError("Progress directory does not exist; initialize with permission")
    with write_lock(path):
        previous = read(path, version, topics, labs)
        event = getattr(args, "event_id", None)
        if event:
            short(event, "event ID", 100)
        if event and event in previous["applied_event_ids"]:
            return previous, False
        if previous["revision"] != args.expected_revision:
            raise StateError(f"Stale revision: file is {previous['revision']}, expected {args.expected_revision}; reload before retrying")
        state = copy.deepcopy(previous)
        mutate(state)
        if event:
            state["applied_event_ids"] = (state["applied_event_ids"] + [event])[-200:]
        state["revision"] += 1
        state["last_saved_at"] = utc_now()
        validate(state, version, topics, labs)
        atomic_bytes(path.with_name(path.name + ".bak"), serialize(previous))
        atomic_bytes(path, serialize(state))
        if read(path, version, topics, labs) != state:
            raise StateError("Write verification failed; inspect backup")
        return state, True


def new_cursor(item_id: str, mode: str) -> dict[str, str | None]:
    step = "step-1" if mode == "Lab" else STEPS[mode][0]
    return {"mode": mode, "checkpoint_id": step, "next_action": f"Start {item_id} {mode.lower()} checkpoint {step}", "resume_note": None}


def get_entry(state: dict[str, Any], item_id: str, labs: dict[str, int], mode: str) -> dict[str, Any]:
    if item_id in labs:
        return state["labs"].setdefault(item_id, {"cursor": new_cursor(item_id, "Lab"), "status": "learning", "steps": {}})
    return state["topics"].setdefault(item_id, {
        "cursor": new_cursor(item_id, mode), "status": "learning", "completed_checkpoints": [],
        "misconceptions": [], "last_practiced_at": None, "next_review_at": None,
    })


def need_active(state: dict[str, Any], topics: set[str], labs: dict[str, int]) -> tuple[str, dict[str, Any]]:
    item_id = state["active"]["item_id"]
    if item_id is None:
        raise StateError("Select a topic or lab before saving a checkpoint")
    return item_id, get_entry(state, item_id, labs, state["active"]["mode"])


def due_queue(state: dict[str, Any], current_date: date) -> list[dict[str, Any]]:
    return sorted((item for item in state["review_queue"] if item["due_date"] <= current_date.isoformat()), key=lambda x: (x["due_date"], x["item_id"]))


def schedule_review(state: dict[str, Any], item_id: str, passed: bool, kind: str, on: date) -> None:
    queue = state["review_queue"]
    existing = next((item for item in queue if item["item_id"] == item_id), None)
    if not passed:
        if existing:
            queue.remove(existing)
        queue.append({"item_id": item_id, "stage": 0, "due_date": on.isoformat()})
    elif kind == "Review" and existing:
        queue.remove(existing)
        if existing["stage"] < 2:
            stage = existing["stage"] + 1
            queue.append({"item_id": item_id, "stage": stage, "due_date": (on + timedelta(days=3 if stage == 1 else 7)).isoformat()})
    queue.sort(key=lambda x: (x["due_date"], x["item_id"]))


def add_mutation_options(parser: argparse.ArgumentParser, *, event: bool = True) -> None:
    parser.add_argument("--expected-revision", required=True, type=int, help="Revision from the latest status/resume read")
    if event:
        parser.add_argument("--event-id", help="Stable retry ID; duplicate event is a no-op")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", help="Private progress JSON path (default: ~/.dotskills/study-mcpa/progress.json)")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="First-time opt-in: create empty private progress file")
    init.add_argument("--approve", action="store_true", help="Required explicit permission to initialize the private file")
    commands.add_parser("status", help="Read the current progress and revision, without writing")
    commands.add_parser("resume", help="Read the pending cursor, without writing")
    review = commands.add_parser("review", help="Read due topics and low-confidence topics")
    review.add_argument("--on-date", type=date.fromisoformat, default=None)
    select = commands.add_parser("select", help="Choose topic ID and resume saved topic checkpoint")
    select.add_argument("--id", required=True)
    select.add_argument("--mode", choices=["Guided", "Practice", "Review", "Lab"])
    add_mutation_options(select)
    checkpoint = commands.add_parser("checkpoint", help="Save a pending or verified completed step")
    checkpoint.add_argument("--step", help="The exact known step ID; omitted means save current cursor")
    checkpoint.add_argument("--outcome", choices=["pending", "completed"], default="pending")
    checkpoint.add_argument("--next-step", help="Explicit next step after completion (defaults to ready)")
    checkpoint.add_argument("--next-action")
    checkpoint.add_argument("--note", help="Short factual reminder, not a tool instruction")
    checkpoint.add_argument("--evidence", help="Required to complete a checkpoint")
    add_mutation_options(checkpoint)
    record = commands.add_parser("record", help="Persist observed Practice/Review/Mock assessment result")
    record.add_argument("--kind", choices=["Practice", "Review", "Mock"], required=True)
    record.add_argument("--id", help="Topic ID for Practice/Review")
    record.add_argument("--attempted", type=int, required=True)
    record.add_argument("--correct", type=int, required=True)
    record.add_argument("--confidence", choices=["low", "medium", "high"])
    record.add_argument("--misconception")
    record.add_argument("--evidence", required=True, help="Brief evidence of actual learner attempt")
    record.add_argument("--self-timed", action="store_true")
    record.add_argument("--on-date", type=date.fromisoformat, default=None)
    add_mutation_options(record)
    lab = commands.add_parser("lab", help="Record proposed, inspected or actually-run lab evidence")
    lab.add_argument("--step", required=True)
    lab.add_argument("--kind", choices=sorted(EVIDENCE_KINDS), required=True)
    lab.add_argument("--evidence", required=True)
    lab.add_argument("--verified", action="store_true")
    lab.add_argument("--approved", action="store_true", help="Required for claiming a step was actually run")
    add_mutation_options(lab)
    mock = commands.add_parser("mock-start", help="Record start of self-managed mock, never question/answer keys")
    mock.add_argument("--length", type=int, choices=[10, 20, 40], required=True)
    add_mutation_options(mock)
    mock_stop = commands.add_parser("mock-stop", help="Mark unfinished mock interrupted, without resetting other progress")
    mock_stop.add_argument("--confirm-stop", action="store_true")
    add_mutation_options(mock_stop)
    reset = commands.add_parser("reset", help="Back up and reset existing progress only with confirmation")
    reset.add_argument("--confirm-reset", action="store_true")
    add_mutation_options(reset)
    correct = commands.add_parser("correct", help="Explicit correction to a topic status")
    correct.add_argument("--id", required=True)
    correct.add_argument("--status", required=True, choices=sorted(TOPIC_STATUS))
    correct.add_argument("--reason", required=True)
    correct.add_argument("--confirm-correction", action="store_true")
    add_mutation_options(correct)
    return parser


def execute(args: argparse.Namespace) -> tuple[dict[str, Any], bool, dict[str, Any]]:
    version, topics, labs = catalog()
    path = state_path(args.state)
    if args.command == "init":
        if not args.approve:
            raise StateError("Initialization requires explicit approval (--approve); no file created")
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with write_lock(path):
            if path.exists():
                raise StateError("Progress file already exists; use status (never silently overwrite)")
            state = initial(version)
            with path.open("x", encoding="utf-8") as out:
                os.chmod(path, 0o600)
                out.write(serialize(state).decode("utf-8"))
                out.flush()
                os.fsync(out.fileno())
            read(path, version, topics, labs)
        return state, True, {"message": "Private study progress initialized"}
    if args.command in {"status", "resume", "review"}:
        state = read(path, version, topics, labs)
        extras = {}
        if args.command == "review":
            extras["due_topics"] = due_queue(state, args.on_date or today())
        if args.command == "resume" and state["mock"] and state["mock"]["status"] == "in_progress":
            extras["warning"] = "Mock was interrupted; exact unanswered questions/answers were not saved. Restart or submit observed answers."
        return state, False, extras

    def mutate(state: dict[str, Any]) -> None:
        if args.command == "select":
            item_id = args.id.upper()
            if item_id not in topics and item_id not in labs:
                raise StateError(f"Unknown topic/lab ID {item_id}; show curriculum menu instead of guessing")
            mode = args.mode or ("Lab" if item_id in labs else "Guided")
            if (item_id in labs) != (mode == "Lab"):
                raise StateError("Only labs can use Lab mode; select a lesson mode for topics")
            entry = get_entry(state, item_id, labs, mode)
            if entry["cursor"]["mode"] != mode:
                entry["cursor"] = new_cursor(item_id, mode)
            state["active"] = {"item_id": item_id, **copy.deepcopy(entry["cursor"])}
        elif args.command == "checkpoint":
            item_id, entry = need_active(state, topics, labs)
            cursor = state["active"]
            step = args.step or cursor["checkpoint_id"]
            if not valid_step(item_id, cursor["mode"], step, labs):
                raise StateError(f"Unknown checkpoint for {item_id}/{cursor['mode']}: {step}")
            if args.outcome == "completed":
                if not args.step or not (args.evidence or "").strip():
                    raise StateError("Completion requires an explicit step and actual evidence")
                next_step = args.next_step or "ready"
                if not valid_step(item_id, cursor["mode"], next_step, labs):
                    raise StateError("Next checkpoint must be a defined step")
                if item_id in topics and step not in entry["completed_checkpoints"]:
