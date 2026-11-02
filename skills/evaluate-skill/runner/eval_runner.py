#!/usr/bin/env python3
"""Active Docker-only Evaluate Skill workflow entry point.

This facade performs offline preparation/configuration directly. Docker
preflight and live execution are dependency-injected trusted-host operations:
the standalone process fails closed unless an approved host embeds them.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any, Callable, Mapping, Optional, Sequence

from contracts import RunPlan
import native_eval


class EvalRunnerError(ValueError):
    """The active workflow request is incomplete, unsafe, or unavailable."""


_COMMANDS = ("inspect", "prepare", "configure", "docker-preflight", "docker-run")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SECURITY_FILE_FIELDS = (
    "run_plan",
    "approval_receipt",
    "capability_inventory",
    "execution_binding",
    "gateway_binding",
    "evidence_binding",
    "image_lock",
    "docker_path",
    "gateway_key",
    "gateway_config",
    "evidence_key",
    "seccomp_policy",
    "executable_inventory",
)
_SECURITY_DIRECTORY_FIELDS = ("prepared_bundle", "artifact_directory")
_DIGEST_FIELDS = (
    "expected_runtime_digest",
    "expected_image_digest",
    "expected_gateway_policy_digest",
    "expected_observer_policy_digest",
    "expected_cleanup_policy_digest",
)


def command_names() -> tuple[str, ...]:
    return _COMMANDS


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "status": "BLOCKED_NOT_RUN",
        "model_executed": False,
        "reason": reason,
    }


def _default_prepare(values: Mapping[str, Any]) -> Mapping[str, Any]:
    harness = {"openai": "codex", "anthropic": "claude"}[values["provider"]]
    bundle = native_eval.prepare(
        SimpleNamespace(
            suite=values["suite"],
            case_id=values["case_id"],
            target_skill=values["target_skill"],
            output=values["output"],
            harness=harness,
            execution_backend="docker",
        ),
        env={},
    )
    return {
        "status": "PREPARED_NOT_RUN",
        "model_executed": False,
        "provider": values["provider"],
        "backend": "docker",
        "bundle": str(bundle),
    }


def _default_configure(values: Mapping[str, Any]) -> Mapping[str, Any]:
    plan_value = native_eval._json_file(values["run_plan"], "run plan")
    plan = RunPlan.from_dict(plan_value)
    if plan.backend != "docker" or plan.provider != values["provider"]:
        raise EvalRunnerError("run plan must match the explicit provider and Docker backend")
    manifest = native_eval.configure_prepared_bundle(values["bundle"], plan)
    return {
        "status": "CONFIGURED_NOT_BOUND",
        "model_executed": False,
        "provider": values["provider"],
        "backend": "docker",
        "bundle": str(Path(values["bundle"]).resolve()),
        "plan_digest": plan.digest(),
        "provider_config_digest": manifest["provider_config_digest"],
    }


def _unembedded_preflight(_values: Mapping[str, Any]) -> Mapping[str, Any]:
    return _blocked(
        "Docker provisioning/probes require an approved trusted-host embedding; "
        "the standalone CLI never starts, pulls, builds, or installs Docker"
    )


def _unembedded_run(_values: Mapping[str, Any]) -> Mapping[str, Any]:
    return _blocked(
        "Docker live execution requires an approved trusted-host embedding and "
        "fresh single-use authorization"
    )


@dataclass(frozen=True)
class EvalRunnerDependencies:
    prepare: Callable[[Mapping[str, Any]], Mapping[str, Any]] = _default_prepare
    configure: Callable[[Mapping[str, Any]], Mapping[str, Any]] = _default_configure
    docker_preflight: Callable[[Mapping[str, Any]], Mapping[str, Any]] = _unembedded_preflight
    docker_run: Callable[[Mapping[str, Any]], Mapping[str, Any]] = _unembedded_run


def _add_security_inputs(parser: argparse.ArgumentParser) -> None:
    for name in _SECURITY_FILE_FIELDS + _SECURITY_DIRECTORY_FIELDS:
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    parser.add_argument("--docker-context", required=True)
    parser.add_argument("--docker-endpoint", required=True)
    for name in _DIGEST_FIELDS:
        parser.add_argument("--" + name.replace("_", "-"), required=True)
    parser.add_argument("--protected-root", type=Path, action="append", required=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("inspect", help="report active backend; never runs Docker or a model")

    prepare = subparsers.add_parser("prepare", help="stage one provider case; no model call")
    prepare.add_argument("--provider", choices=("openai", "anthropic"), required=True)
    prepare.add_argument("--suite", type=Path, required=True)
    prepare.add_argument("--case-id", required=True)
    prepare.add_argument("--target-skill", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)

    configure = subparsers.add_parser(
        "configure", help="materialize approved provider settings; no model call"
    )
    configure.add_argument("--provider", choices=("openai", "anthropic"), required=True)
    configure.add_argument("--bundle", type=Path, required=True)
    configure.add_argument("--run-plan", type=Path, required=True)

    preflight = subparsers.add_parser(
        "docker-preflight", help="run approved no-model Docker probes"
    )
    _add_security_inputs(preflight)

    run = subparsers.add_parser(
        "docker-run", help="run one authorized Docker evaluation arm"
    )
    _add_security_inputs(run)
    run.add_argument("--preflight-artifact", type=Path, required=True)
    run.add_argument("--live-authorization", type=Path, required=True)
    return parser


def _existing_path(path: Path, name: str, *, directory: bool) -> Path:
    value = Path(path)
    if not value.is_absolute() or value.is_symlink():
        raise EvalRunnerError(f"{name} must be an explicit absolute non-symlink path")
    valid = value.is_dir() if directory else value.is_file()
    if not valid:
        kind = "directory" if directory else "regular file"
        raise EvalRunnerError(f"{name} must be an existing {kind}")
    return value


def _validated_values(args: argparse.Namespace) -> dict[str, Any]:
    values = vars(args).copy()
    action = values.pop("action")
    values["action"] = action
    if action == "prepare":
        _existing_path(values["suite"], "suite", directory=False)
        _existing_path(values["target_skill"], "target skill", directory=True)
    elif action == "configure":
        _existing_path(values["bundle"], "bundle", directory=True)
        _existing_path(values["run_plan"], "run plan", directory=False)
    elif action in ("docker-preflight", "docker-run"):
        for name in _SECURITY_FILE_FIELDS:
            _existing_path(values[name], name, directory=False)
        for name in _SECURITY_DIRECTORY_FIELDS:
            _existing_path(values[name], name, directory=True)
        for path in values["protected_root"]:
            _existing_path(path, "protected root", directory=True)
        if not values["docker_endpoint"].startswith("unix:///"):
            raise EvalRunnerError("Docker endpoint must be one explicit local Unix socket")
        for name in _DIGEST_FIELDS:
            if _DIGEST.fullmatch(values[name]) is None:
                raise EvalRunnerError(f"{name} must be a lowercase SHA-256 digest")
        if action == "docker-run":
            _existing_path(values["preflight_artifact"], "preflight artifact", directory=False)
            _existing_path(values["live_authorization"], "live authorization", directory=False)
    return values


def _inspect_payload() -> dict[str, Any]:
    return {
        "status": "DOCKER_DESIGN_PENDING",
        "active_backend": "docker",
        "fallback_backend": None,
        "model_executed": False,
        "real_docker_probes_passed": False,
        "implicit_actions": [],
        "next_gate": "separate approval for Docker provisioning and real no-model probes",
    }


def _exit_code(payload: Mapping[str, Any]) -> int:
    status = payload.get("status")
    return 2 if status in ("BLOCKED_NOT_RUN", "INCOMPLETE", "INFRA_ERROR") else 0


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    dependencies: EvalRunnerDependencies = EvalRunnerDependencies(),
) -> int:
    try:
        args = _parser().parse_args(argv)
        values = _validated_values(args)
        if args.action == "inspect":
            payload = _inspect_payload()
        elif args.action == "prepare":
            payload = dependencies.prepare(values)
        elif args.action == "configure":
            payload = dependencies.configure(values)
        elif args.action == "docker-preflight":
            payload = dependencies.docker_preflight(values)
        else:
            payload = dependencies.docker_run(values)
        if not isinstance(payload, Mapping) or not isinstance(payload.get("status"), str):
            raise EvalRunnerError("workflow dependency returned an invalid status payload")
        output = dict(payload)
    except SystemExit:
        output = _blocked("explicit required CLI input is missing or invalid")
    except Exception as exc:
        output = _blocked(str(exc) or type(exc).__name__)
    print(json.dumps(output, sort_keys=True))
    return _exit_code(output)


if __name__ == "__main__":
    raise SystemExit(main())
