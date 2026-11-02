"""Strict v0.2 run-plan, approval, and enforcement contracts."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping, Tuple


class ContractError(ValueError):
    """A contract is incomplete, malformed, or outside its declared scope."""


_PROFILES = frozenset(("no-tool", "read-only", "disposable-write", "mock-external"))
_BACKENDS = frozenset(("native", "docker"))
_RESOURCE_LIMITS = frozenset(
    ("max_seconds", "max_turns", "max_output_bytes", "max_cost_usd")
)
_PROBE_STATUSES = frozenset(("PASS", "FAIL", "UNKNOWN", "INCOMPLETE"))


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise ContractError(f"{name} field names must be strings")
    return value


def _exact_fields(value: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    actual = frozenset(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise ContractError(f"{name} missing fields: {', '.join(missing)}")
    if unknown:
        raise ContractError(f"{name} unknown fields: {', '.join(unknown)}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str) -> Tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractError(f"{name} must be an array")
    result = tuple(_text(item, f"{name} item") for item in value)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return result


def _canonical_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class CapabilityRequirements:
    profile: str
    filesystem_read: Tuple[str, ...]
    filesystem_write: Tuple[str, ...]
    shell: bool
    network: Tuple[str, ...]
    mock_tools: Tuple[str, ...]
    credentials: Tuple[str, ...]
    side_effects: Tuple[str, ...]
    evidence: Tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CapabilityRequirements":
        value = _mapping(value, "capabilities")
        expected = frozenset(
            (
                "profile",
                "filesystem_read",
                "filesystem_write",
                "shell",
                "network",
                "mock_tools",
                "credentials",
                "side_effects",
                "evidence",
            )
        )
        _exact_fields(value, expected, "capabilities")
        profile = _text(value["profile"], "capabilities.profile")
        if profile not in _PROFILES:
            raise ContractError(f"unsupported capability profile: {profile}")
        if not isinstance(value["shell"], bool):
            raise ContractError("capabilities.shell must be a boolean")
        return cls(
            profile=profile,
            filesystem_read=_strings(value["filesystem_read"], "capabilities.filesystem_read"),
            filesystem_write=_strings(value["filesystem_write"], "capabilities.filesystem_write"),
            shell=value["shell"],
            network=_strings(value["network"], "capabilities.network"),
            mock_tools=_strings(value["mock_tools"], "capabilities.mock_tools"),
            credentials=_strings(value["credentials"], "capabilities.credentials"),
            side_effects=_strings(value["side_effects"], "capabilities.side_effects"),
            evidence=_strings(value["evidence"], "capabilities.evidence"),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "filesystem_read": list(self.filesystem_read),
            "filesystem_write": list(self.filesystem_write),
            "shell": self.shell,
            "network": list(self.network),
            "mock_tools": list(self.mock_tools),
            "credentials": list(self.credentials),
            "side_effects": list(self.side_effects),
            "evidence": list(self.evidence),
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


@dataclass(frozen=True)
class RunPlan:
    schema_version: str
    case_id: str
    case_revision: str
    rubric_revision: str
    skill_revision: str
    fixture_revision: str
    provider: str
    provider_version: str
    model: str
    model_version: str
    adapter: str
    adapter_version: str
    backend: str
    capabilities: CapabilityRequirements
    resource_limits: Mapping[str, float]
    comparison_arms: Tuple[str, ...]
    evidence_requirements: Tuple[str, ...]
    cleanup_requirements: Tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RunPlan":
        value = _mapping(value, "run plan")
        expected = frozenset(
            (
                "schema_version",
                "case_id",
                "case_revision",
                "rubric_revision",
                "skill_revision",
                "fixture_revision",
                "provider",
                "provider_version",
                "model",
                "model_version",
                "adapter",
                "adapter_version",
                "backend",
                "capabilities",
                "resource_limits",
                "comparison_arms",
                "evidence_requirements",
                "cleanup_requirements",
            )
        )
        _exact_fields(value, expected, "run plan")
        backend = _text(value["backend"], "run plan.backend")
        if backend not in _BACKENDS:
            raise ContractError(f"unsupported backend: {backend}")
        limits = _mapping(value["resource_limits"], "run plan.resource_limits")
        _exact_fields(limits, _RESOURCE_LIMITS, "run plan.resource_limits")
        normalized_limits = {}
        for name in sorted(_RESOURCE_LIMITS):
            limit = limits[name]
            if isinstance(limit, bool) or not isinstance(limit, (int, float)) or limit <= 0:
                raise ContractError(f"run plan.resource_limits.{name} must be positive")
            normalized_limits[name] = limit
        text_fields = {
            name: _text(value[name], f"run plan.{name}")
            for name in (
                "schema_version",
                "case_id",
                "case_revision",
                "rubric_revision",
                "skill_revision",
                "fixture_revision",
                "provider",
                "provider_version",
                "model",
                "model_version",
                "adapter",
                "adapter_version",
            )
        }
        return cls(
            **text_fields,
            backend=backend,
            capabilities=CapabilityRequirements.from_dict(value["capabilities"]),
            resource_limits=MappingProxyType(normalized_limits),
            comparison_arms=_strings(value["comparison_arms"], "run plan.comparison_arms"),
            evidence_requirements=_strings(
                value["evidence_requirements"], "run plan.evidence_requirements"
            ),
            cleanup_requirements=_strings(
                value["cleanup_requirements"], "run plan.cleanup_requirements"
            ),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "case_id": self.case_id,
            "case_revision": self.case_revision,
            "rubric_revision": self.rubric_revision,
            "skill_revision": self.skill_revision,
            "fixture_revision": self.fixture_revision,
            "provider": self.provider,
            "provider_version": self.provider_version,
            "model": self.model,
            "model_version": self.model_version,
            "adapter": self.adapter,
            "adapter_version": self.adapter_version,
            "backend": self.backend,
            "capabilities": self.capabilities.canonical_payload(),
            "resource_limits": dict(self.resource_limits),
            "comparison_arms": list(self.comparison_arms),
            "evidence_requirements": list(self.evidence_requirements),
            "cleanup_requirements": list(self.cleanup_requirements),
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


@dataclass(frozen=True)
class ApprovalReceipt:
    schema_version: str
    plan_digest: str
    approved_by: str
    provider: str
    model: str
    adapter: str
    backend: str
    capability_profile: str
    capability_digest: str
    side_effects: Tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ApprovalReceipt":
        value = _mapping(value, "approval receipt")
        expected = frozenset(
            (
                "schema_version",
                "plan_digest",
                "approved_by",
                "provider",
                "model",
                "adapter",
                "backend",
                "capability_profile",
                "capability_digest",
                "side_effects",
            )
        )
        _exact_fields(value, expected, "approval receipt")
        backend = _text(value["backend"], "approval receipt.backend")
        profile = _text(value["capability_profile"], "approval receipt.capability_profile")
        if backend not in _BACKENDS:
            raise ContractError(f"unsupported approval backend: {backend}")
        if profile not in _PROFILES:
            raise ContractError(f"unsupported approval profile: {profile}")
        return cls(
            schema_version=_text(value["schema_version"], "approval receipt.schema_version"),
            plan_digest=_text(value["plan_digest"], "approval receipt.plan_digest"),
            approved_by=_text(value["approved_by"], "approval receipt.approved_by"),
            provider=_text(value["provider"], "approval receipt.provider"),
            model=_text(value["model"], "approval receipt.model"),
            adapter=_text(value["adapter"], "approval receipt.adapter"),
            backend=backend,
            capability_profile=profile,
            capability_digest=_text(
                value["capability_digest"], "approval receipt.capability_digest"
            ),
            side_effects=_strings(value["side_effects"], "approval receipt.side_effects"),
        )

    def validate_for(self, plan: RunPlan) -> None:
        comparisons = {
            "schema_version": (self.schema_version, plan.schema_version),
            "plan_digest": (self.plan_digest, plan.digest()),
            "provider": (self.provider, plan.provider),
            "model": (self.model, plan.model),
            "adapter": (self.adapter, plan.adapter),
            "backend": (self.backend, plan.backend),
            "capability_profile": (self.capability_profile, plan.capabilities.profile),
            "capability_digest": (self.capability_digest, plan.capabilities.digest()),
            "side_effects": (self.side_effects, plan.capabilities.side_effects),
        }
        mismatches = sorted(
            name for name, (approved, planned) in comparisons.items() if approved != planned
        )
        if mismatches:
            raise ContractError(f"approval receipt scope mismatch: {', '.join(mismatches)}")


@dataclass(frozen=True)
class EnforcementReceipt:
    schema_version: str
    plan_digest: str
    verified_by: str
    verifier_version: str
    provider: str
    provider_version: str
    model: str
    model_version: str
    adapter: str
    adapter_version: str
    backend: str
    backend_version: str
    capability_profile: str
    effective_policy_digest: str
    workspace_id: str
    probe_results: Mapping[str, str]
    enabled_tools: Tuple[str, ...]
    disabled_tools: Tuple[str, ...]
    state_verification_method: str
    cleanup_method: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "EnforcementReceipt":
        value = _mapping(value, "enforcement receipt")
        expected = frozenset(
            (
                "schema_version",
                "plan_digest",
                "verified_by",
                "verifier_version",
                "provider",
                "provider_version",
                "model",
                "model_version",
                "adapter",
                "adapter_version",
                "backend",
                "backend_version",
                "capability_profile",
                "effective_policy_digest",
                "workspace_id",
                "probe_results",
                "enabled_tools",
                "disabled_tools",
                "state_verification_method",
                "cleanup_method",
            )
        )
        _exact_fields(value, expected, "enforcement receipt")
        text = {
            name: _text(value[name], f"enforcement receipt.{name}")
            for name in (
                "schema_version",
                "plan_digest",
                "verified_by",
                "verifier_version",
                "provider",
                "provider_version",
                "model",
                "model_version",
                "adapter",
                "adapter_version",
                "backend",
                "backend_version",
                "capability_profile",
                "effective_policy_digest",
                "workspace_id",
                "state_verification_method",
                "cleanup_method",
            )
        }
        if text["backend"] not in _BACKENDS:
            raise ContractError(f"unsupported enforcement backend: {text['backend']}")
        if text["capability_profile"] not in _PROFILES:
            raise ContractError(
                f"unsupported enforcement profile: {text['capability_profile']}"
            )
        if text["verified_by"] in (text["provider"], text["adapter"]):
            raise ContractError("enforcement verifier must be independent of provider and adapter")
        probes = _mapping(value["probe_results"], "enforcement receipt.probe_results")
        if not probes:
            raise ContractError("enforcement receipt requires probe results")
        normalized_probes = {}
        for probe_id, status in probes.items():
            probe_id = _text(probe_id, "enforcement receipt probe id")
            status = _text(status, f"enforcement receipt probe {probe_id}")
            if status not in _PROBE_STATUSES:
                raise ContractError(f"unknown probe status for {probe_id}: {status}")
            normalized_probes[probe_id] = status
        return cls(
            **text,
            probe_results=MappingProxyType(dict(sorted(normalized_probes.items()))),
            enabled_tools=_strings(value["enabled_tools"], "enforcement receipt.enabled_tools"),
            disabled_tools=_strings(
                value["disabled_tools"], "enforcement receipt.disabled_tools"
            ),
        )
