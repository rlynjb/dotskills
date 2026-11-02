"""Immutable mock-tool authorization for the mock-external profile."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping, Tuple

from contracts import RunPlan


class MockDispatchError(ValueError):
    """The host-owned mock registry is malformed."""


_IMPLEMENTATIONS = frozenset(("record-note-v1", "read-record-v1"))
_REQUEST_FIELDS = frozenset(("tool", "effect", "destination", "route", "arguments"))


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MockDispatchError(f"{name} must be a non-empty string")
    return value


@dataclass(frozen=True)
class MockTool:
    tool_id: str
    effect: str
    destination: str
    implementation: str


@dataclass(frozen=True)
class MockRegistry:
    schema_version: str
    tools: Mapping[str, MockTool]
    write_allowlist: Tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "MockRegistry":
        if not isinstance(value, Mapping):
            raise MockDispatchError("mock registry must be an object")
        unknown = sorted(set(value) - {"schema_version", "tools", "write_allowlist"})
        missing = sorted({"schema_version", "tools"} - set(value))
        if unknown or missing:
            raise MockDispatchError(
                f"mock registry fields invalid; missing={missing}, unknown={unknown}"
            )
        raw_tools = value["tools"]
        if not isinstance(raw_tools, list) or not raw_tools:
            raise MockDispatchError("mock registry tools must be a non-empty array")
        tools = {}
        for raw in raw_tools:
            if not isinstance(raw, Mapping) or set(raw) != {
                "id", "effect", "destination", "implementation"
            }:
                raise MockDispatchError("mock tool fields are invalid")
            tool_id = _text(raw["id"], "mock tool id")
            effect = _text(raw["effect"], "mock tool effect")
            destination = _text(raw["destination"], "mock tool destination")
            implementation = _text(raw["implementation"], "mock implementation")
            if not tool_id.startswith("mock.") or len(tool_id) <= 5:
                raise MockDispatchError("mock tool ids must use the mock.* namespace")
            if effect not in ("read", "write"):
                raise MockDispatchError("mock tool effect must be read or write")
            if not destination.startswith("mock://"):
                raise MockDispatchError("mock tool destination must use mock://")
            if implementation not in _IMPLEMENTATIONS:
                raise MockDispatchError("mock implementation is not host-owned")
            if tool_id in tools:
                raise MockDispatchError("duplicate mock tool id")
            tools[tool_id] = MockTool(tool_id, effect, destination, implementation)
        raw_writes = value.get("write_allowlist", [])
        if not isinstance(raw_writes, list) or any(not isinstance(item, str) for item in raw_writes):
            raise MockDispatchError("write_allowlist must be an array of tool ids")
        write_allowlist = tuple(raw_writes)
        if len(write_allowlist) != len(set(write_allowlist)):
            raise MockDispatchError("write_allowlist must not contain duplicates")
        if any(item not in tools or tools[item].effect != "write" for item in write_allowlist):
            raise MockDispatchError("write_allowlist must name registered write tools")
        return cls(
            _text(value["schema_version"], "mock registry schema_version"),
            MappingProxyType(tools),
            write_allowlist,
        )


@dataclass(frozen=True)
class ToolDecision:
    decision: str
    reason: str
    event: dict[str, Any]


def _event(tool: Any, *, authorized: bool, outcome: str, reason: str, **values: Any):
    event = {
        "type": "tool_attempt",
        "capability": "mock_tools",
        "tool": tool if isinstance(tool, str) else "invalid",
        "authorized": authorized,
        "outcome": outcome,
        "reason": reason,
    }
    event.update(values)
    return event


def _deny(tool: Any, reason: str) -> ToolDecision:
    return ToolDecision("deny", reason, _event(tool, authorized=False, outcome="blocked", reason=reason))


def authorize_tool_call(
    registry: MockRegistry, plan: RunPlan, request: Mapping[str, Any]
) -> ToolDecision:
    """Authorize one host-classified request without trusting request metadata."""
    if not isinstance(registry, MockRegistry) or not isinstance(plan, RunPlan):
        return _deny(None, "trusted_registry_and_plan_required")
    if plan.capabilities.profile != "mock-external":
        return _deny(None, "mock_external_profile_required")
    if not isinstance(request, Mapping) or set(request) != _REQUEST_FIELDS:
        return _deny(request.get("tool") if isinstance(request, Mapping) else None, "invalid_request")
    tool_id = request.get("tool")
    if not isinstance(tool_id, str) or tool_id not in registry.tools:
        return _deny(tool_id, "tool_not_registered")
    tool = registry.tools[tool_id]
    if tool_id not in plan.capabilities.mock_tools:
        return _deny(tool_id, "tool_not_approved_by_plan")
    if request.get("route") != "mock-dispatch":
        return _deny(tool_id, "bypass_route_denied")
    if request.get("effect") != tool.effect:
        return _deny(tool_id, "effect_mismatch")
    if request.get("destination") != tool.destination:
        return _deny(tool_id, "destination_mismatch")
    if tool.effect == "write" and tool_id not in registry.write_allowlist:
        return _deny(tool_id, "write_not_allowlisted")
    arguments = request.get("arguments")
    if not isinstance(arguments, Mapping):
        return _deny(tool_id, "arguments_must_be_object")
    try:
        encoded = json.dumps(
            arguments, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    except (TypeError, ValueError):
        return _deny(tool_id, "arguments_not_serializable")
    event = _event(
        tool_id,
        authorized=True,
        outcome="mocked",
        reason="host_owned_mock",
        effect=tool.effect,
        destination=tool.destination,
        arguments_digest=hashlib.sha256(encoded).hexdigest(),
    )
    return ToolDecision("allow", "host_owned_mock", event)
