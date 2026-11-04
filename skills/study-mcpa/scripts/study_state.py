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
