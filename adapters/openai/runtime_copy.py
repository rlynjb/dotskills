"""Runtime-only skill distribution: never copy evaluator-only evals/."""
from __future__ import annotations
from pathlib import Path


def ignore_evaluator_material(source: Path):
    root = source.resolve()

    def ignore(directory, names):
        return {"evals"} if Path(directory).resolve() == root and "evals" in names else set()

    return ignore
