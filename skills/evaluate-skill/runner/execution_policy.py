"""Fail-closed policy assessment for an approved Evaluate Skill run."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional, Tuple

from capability_inventory import CapabilityInventory, InventoryError, PlatformFingerprint
from contracts import ApprovalReceipt, EnforcementReceipt, RunPlan


_SCHEMA_VERSION = "0.2"
_TOOL_SURFACES = (
    "filesystem_read",
    "filesystem_write",
    "shell",
    "network",
    "mock_tools",
)
_CAPABILITY_EVIDENCE = frozenset(("action-trace", "protected-state"))
_RUN_EVIDENCE = frozenset(("provider-result", "host-audit"))
_CLEANUP_REQUIREMENTS = frozenset(("workspace-removed", "state-verified"))
_STATE_VERIFICATION_METHOD = "tree-digest-v1"
_CLEANUP_METHOD = "remove-and-verify-v1"


@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    backend: Optional[str]
    reasons: Tuple[str, ...]


def _reason(reasons: list[str], field: str, detail: str) -> None:
    reasons.append(f"{field}: {detail}")


def _compare(reasons: list[str], field: str, actual: object, expected: object) -> None:
    if actual != expected:
        _reason(reasons, field, "mismatch")


def _required_tool_routes(plan: RunPlan) -> Tuple[frozenset[str], frozenset[str]]:
    capabilities = plan.capabilities
    required = {
        "filesystem_read": bool(capabilities.filesystem_read),
        "filesystem_write": bool(capabilities.filesystem_write),
        "shell": capabilities.shell,
        "network": bool(capabilities.network),
        "mock_tools": bool(capabilities.mock_tools),
    }
    enabled = frozenset(name for name, is_required in required.items() if is_required)
    disabled = frozenset(name for name in _TOOL_SURFACES if name not in enabled)
    return enabled, disabled


def assess_run(
    plan: RunPlan,
    approval: Optional[ApprovalReceipt],
    enforcement: object,
    inventory: CapabilityInventory,
    *,
    at: Optional[datetime] = None,
    observed_versions: Optional[Mapping[str, Optional[str]]] = None,
    observed_platform: Optional[PlatformFingerprint] = None,
) -> PolicyDecision:
    """Assess exact approved inputs without changing provider or backend."""

    reasons: list[str] = []
    if not isinstance(plan, RunPlan):
        return PolicyDecision("BLOCKED", None, ("run_plan: required RunPlan",))
    if not isinstance(approval, ApprovalReceipt):
        _reason(reasons, "approval_receipt", "required ApprovalReceipt")
    if not isinstance(enforcement, EnforcementReceipt):
        _reason(reasons, "enforcement_receipt", "required EnforcementReceipt")
    if not isinstance(inventory, CapabilityInventory):
        _reason(reasons, "capability_inventory", "required CapabilityInventory")
    if reasons:
        return PolicyDecision("BLOCKED", None, tuple(reasons))

    assert approval is not None
    assert isinstance(enforcement, EnforcementReceipt)

    if plan.schema_version != _SCHEMA_VERSION:
        _reason(reasons, "plan.schema_version", "unsupported")

    approval_scope = {
        "schema_version": plan.schema_version,
        "plan_digest": plan.digest(),
        "provider": plan.provider,
        "model": plan.model,
        "adapter": plan.adapter,
        "backend": plan.backend,
        "capability_profile": plan.capabilities.profile,
        "capability_digest": plan.capabilities.digest(),
        "side_effects": plan.capabilities.side_effects,
    }
    for field, expected in approval_scope.items():
        _compare(reasons, f"approval.{field}", getattr(approval, field), expected)

    enforcement_scope = {
        "schema_version": plan.schema_version,
        "plan_digest": plan.digest(),
        "provider": plan.provider,
        "provider_version": plan.provider_version,
        "model": plan.model,
        "model_version": plan.model_version,
        "adapter": plan.adapter,
        "adapter_version": plan.adapter_version,
        "backend": plan.backend,
        "capability_profile": plan.capabilities.profile,
        "effective_policy_digest": plan.capabilities.digest(),
    }
    for field, expected in enforcement_scope.items():
        _compare(reasons, f"enforcement.{field}", getattr(enforcement, field), expected)
    if approval.run_nonce != enforcement.run_nonce:
        _reason(reasons, "receipt.run_nonce", "approval and enforcement nonce mismatch")
    if not approval.is_valid_at(at):
        _reason(reasons, "approval.validity", "receipt is not current")
    if not enforcement.is_valid_at(at):
        _reason(reasons, "enforcement.validity", "receipt is not current")

    provider_key = inventory.provider_for_plan(plan.provider, plan.adapter)
    if provider_key is None:
        _reason(reasons, "inventory.provider_adapter", "no exact pinned match")
    else:
        descriptor = inventory.providers[provider_key]
        _compare(
            reasons,
            "plan.provider_version",
            plan.provider_version,
            descriptor.provider_version,
        )
        _compare(
            reasons,
            "plan.adapter_version",
            plan.adapter_version,
            descriptor.adapter_version,
        )
        _compare(
            reasons,
            f"inventory.required_versions.{provider_key}",
            descriptor.provider_version,
            inventory.required_versions.get(provider_key),
        )
        _compare(
            reasons,
            "inventory.required_versions.promptfoo",
            descriptor.adapter_version,
            inventory.required_versions.get("promptfoo"),
        )
        if observed_versions is None:
            _reason(reasons, "installed_versions", "required observations missing")
        else:
            for tool in (provider_key, "promptfoo"):
                _compare(
                    reasons,
                    f"installed_versions.{tool}",
                    observed_versions.get(tool),
                    inventory.required_versions.get(tool),
                )

    if observed_platform is None:
        _reason(reasons, "installed_platform", "required observation missing")
    elif observed_platform != inventory.platform:
        _reason(reasons, "installed_platform", "exact fingerprint mismatch")

    for item in plan.capabilities.evidence:
        if item not in _CAPABILITY_EVIDENCE:
            _reason(reasons, f"capabilities.evidence.{item}", "unsupported")
    for item in plan.evidence_requirements:
        if item not in _RUN_EVIDENCE:
            _reason(reasons, f"evidence_requirements.{item}", "unsupported")
    for item in plan.cleanup_requirements:
        if item not in _CLEANUP_REQUIREMENTS:
            _reason(reasons, f"cleanup_requirements.{item}", "unsupported")

    if provider_key is not None:
        for capability in inventory.capabilities:
            try:
                claim = inventory.claim(
                    provider_key,
                    plan.backend,
                    plan.capabilities.profile,
                    capability,
                )
            except InventoryError:
                _reason(reasons, f"capabilities.{capability}", "missing inventory claim")
                continue
            if claim.status != "verified":
                _reason(
                    reasons,
                    f"capabilities.{capability}",
                    f"inventory status {claim.status}",
                )
            for probe_id in claim.required_probes:
                if enforcement.probe_results.get(probe_id) != "PASS":
                    _reason(
                        reasons,
                        f"enforcement.probe_results.{probe_id}",
                        "missing or not PASS",
                    )

    if plan.capabilities.profile in ("no-tool", "read-only", "mock-external"):
        if enforcement.probe_results.get("write-inside-workspace") != "PASS":
            _reason(
                reasons,
                "enforcement.probe_results.write-inside-workspace",
                "missing or not PASS",
            )

    expected_enabled, expected_disabled = _required_tool_routes(plan)
    if frozenset(enforcement.enabled_tools) != expected_enabled:
        _reason(reasons, "enforcement.enabled_tools", "does not match approved surfaces")
    if frozenset(enforcement.disabled_tools) != expected_disabled:
        _reason(reasons, "enforcement.disabled_tools", "does not match denied surfaces")
    if enforcement.state_verification_method != _STATE_VERIFICATION_METHOD:
        _reason(reasons, "enforcement.state_verification_method", "unsupported")
    if enforcement.cleanup_method != _CLEANUP_METHOD:
        _reason(reasons, "enforcement.cleanup_method", "unsupported")

    if reasons:
        return PolicyDecision("BLOCKED", None, tuple(dict.fromkeys(reasons)))
    return PolicyDecision("APPROVED", plan.backend, ())
