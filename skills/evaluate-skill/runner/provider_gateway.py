"""Scoped provider-auth gateway with signed, single-session run grants."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import stat
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional, Tuple

from docker_contracts import DockerGatewayBinding


class GatewayError(ValueError):
    """The provider gateway request is malformed, unauthorized, or replayed."""


_PROVIDER_ENDPOINT = "https://api.openai.com/v1/responses"
_INTERNAL_BASE_URL = "http://provider-gateway:8080/v1"
_REQUEST_FIELDS = frozenset(
    (
        "request_id",
        "plan_digest",
        "session_id",
        "nonce",
        "provider",
        "model",
        "model_version",
        "role",
        "operation",
        "request_bytes",
        "expected_output_bytes",
        "turn",
        "prompt",
    )
)
_MAX_LEDGER_BYTES = 64 * 1024


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise GatewayError("grant timestamp is invalid") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise GatewayError("grant timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def _current(at: Optional[datetime]) -> datetime:
    current = datetime.now(timezone.utc) if at is None else at
    if current.tzinfo is None or current.utcoffset() is None:
        raise GatewayError("authorization time must include a timezone")
    return current.astimezone(timezone.utc)


def _key(value: bytes) -> bytes:
    if not isinstance(value, bytes) or len(value) < 32:
        raise GatewayError("gateway HMAC key must contain at least 32 bytes")
    return value


@dataclass(frozen=True)
class RunGrant:
    schema_version: str
    binding_digest: str
    plan_digest: str
    provider: str
    model: str
    model_version: str
    role: str
    operation: str
    limits: Mapping[str, float]
    nonce: str
    session_id: str
    issued_at: str
    expires_at: str
    key_id: str
    signature: str

    @classmethod
    def issue(
        cls, binding: DockerGatewayBinding, key: bytes, *, key_id: str
    ) -> "RunGrant":
        if not isinstance(binding, DockerGatewayBinding):
            raise GatewayError("DockerGatewayBinding is required")
        if not isinstance(key_id, str) or not key_id.strip():
            raise GatewayError("gateway key_id is required")
        unsigned = {
            "schema_version": "0.4",
            "binding_digest": binding.digest(),
            "plan_digest": binding.plan_digest,
            "provider": binding.provider,
            "model": binding.model,
            "model_version": binding.model_version,
            "role": binding.role,
            "operation": binding.operation,
            "limits": dict(binding.limits),
            "nonce": binding.single_use_nonce,
            "session_id": binding.session_id,
            "issued_at": binding.issued_at,
            "expires_at": binding.expires_at,
            "key_id": key_id,
        }
        signature = hmac.new(_key(key), _canonical_json(unsigned), hashlib.sha256).hexdigest()
        fields = dict(unsigned)
        fields["limits"] = MappingProxyType(dict(binding.limits))
        return cls(**fields, signature=signature)

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "binding_digest": self.binding_digest,
            "plan_digest": self.plan_digest,
            "provider": self.provider,
            "model": self.model,
            "model_version": self.model_version,
            "role": self.role,
            "operation": self.operation,
            "limits": dict(self.limits),
            "nonce": self.nonce,
            "session_id": self.session_id,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "key_id": self.key_id,
        }

    def canonical_payload(self) -> dict[str, Any]:
        return {**self.unsigned_payload(), "signature": self.signature}

    def to_token(self) -> str:
        encoded = base64.urlsafe_b64encode(_canonical_json(self.canonical_payload()))
        return encoded.rstrip(b"=").decode("ascii")

    def verify(
        self,
        binding: DockerGatewayBinding,
        key: bytes,
        *,
        at: Optional[datetime] = None,
    ) -> bool:
        try:
            current = _current(at)
            expected_scope = {
                "schema_version": "0.4",
                "binding_digest": binding.digest(),
                "plan_digest": binding.plan_digest,
                "provider": binding.provider,
                "model": binding.model,
                "model_version": binding.model_version,
                "role": binding.role,
                "operation": binding.operation,
                "limits": dict(binding.limits),
                "nonce": binding.single_use_nonce,
                "session_id": binding.session_id,
                "issued_at": binding.issued_at,
                "expires_at": binding.expires_at,
            }
            actual_scope = self.unsigned_payload()
            actual_scope.pop("key_id")
            if actual_scope != expected_scope:
                return False
            expected_signature = hmac.new(
                _key(key), _canonical_json(self.unsigned_payload()), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(self.signature, expected_signature):
                return False
            return _timestamp(self.issued_at) <= current < _timestamp(self.expires_at)
        except (GatewayError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class GatewayDecision:
    allowed: bool
    status: str
    reason: str
    request_id: str
    session_id: str

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "status": self.status,
            "reason": self.reason,
            "request_id": self.request_id,
            "session_id": self.session_id,
        }


@dataclass(frozen=True)
class GatewayAuditEvent:
    event_type: str
    decision: str
    request_id: str
    session_id: str
    plan_digest: str
    provider: str
    model_version: str
    role: str
    operation: str
    details: Mapping[str, Any]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "decision": self.decision,
            "request_id": self.request_id,
            "session_id": self.session_id,
            "plan_digest": self.plan_digest,
            "provider": self.provider,
            "model_version": self.model_version,
            "role": self.role,
            "operation": self.operation,
            **dict(self.details),
        }


@dataclass(frozen=True)
class GatewayResult:
    decision: GatewayDecision
    response: Mapping[str, Any]
    events: Tuple[GatewayAuditEvent, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "decision": self.decision.canonical_payload(),
            "response": dict(self.response),
            "events": [event.canonical_payload() for event in self.events],
        }


class GatewayReplayState:
    """Host-owned, lock-protected replay state outside workload storage."""

    def __init__(self, root: Path):
        path = Path(root)
        if not path.is_absolute() or path.is_symlink() or not path.is_dir():
            raise GatewayError("gateway replay ledger must be a real absolute directory")
        self.root = path

    def consume(
        self, *, nonce: str, session_id: str, request_id: str, max_requests: int
    ) -> None:
        ledger_name = hashlib.sha256(nonce.encode("utf-8")).hexdigest() + ".json"
        path = self.root / ledger_name
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(path, flags, 0o600)
        except OSError as exc:
            raise GatewayError(f"cannot open gateway replay ledger: {exc}") from None
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                raise GatewayError("gateway replay ledger entry must be a regular file")
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            os.lseek(descriptor, 0, os.SEEK_SET)
            raw = os.read(descriptor, _MAX_LEDGER_BYTES + 1)
            if len(raw) > _MAX_LEDGER_BYTES:
                raise GatewayError("gateway replay ledger entry is oversized")
            if raw:
                try:
                    state = json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise GatewayError("gateway replay ledger entry is malformed") from None
                if not isinstance(state, dict) or set(state) != {
                    "session_id",
                    "request_ids",
                }:
                    raise GatewayError("gateway replay ledger entry has unknown fields")
                if state["session_id"] != session_id:
                    raise GatewayError("run grant was replayed for another session")
                request_ids = state["request_ids"]
                if not isinstance(request_ids, list) or not all(
                    isinstance(item, str) for item in request_ids
                ):
                    raise GatewayError("gateway replay request ledger is malformed")
            else:
                request_ids = []
                state = {"session_id": session_id, "request_ids": request_ids}
            if request_id in request_ids:
                raise GatewayError("duplicate gateway request")
            if len(request_ids) >= max_requests:
                raise GatewayError("gateway request budget exhausted")
            request_ids.append(request_id)
            encoded = _canonical_json(state)
            os.lseek(descriptor, 0, os.SEEK_SET)
            os.ftruncate(descriptor, 0)
            os.write(descriptor, encoded)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _decision(allowed: bool, reason: str, request: Mapping[str, Any]) -> GatewayDecision:
    request_id = request.get("request_id", "unknown")
    session_id = request.get("session_id", "unknown")
    return GatewayDecision(
        allowed=allowed,
        status="ALLOWED" if allowed else "BLOCKED_NOT_RUN",
        reason=reason,
        request_id=request_id if isinstance(request_id, str) else "unknown",
        session_id=session_id if isinstance(session_id, str) else "unknown",
    )


def authorize_gateway_request(
    binding: DockerGatewayBinding,
    grant: RunGrant,
    request: Mapping[str, Any],
    replay_state: GatewayReplayState,
    *,
    grant_key: bytes,
    at: Optional[datetime] = None,
) -> GatewayDecision:
    if not isinstance(binding, DockerGatewayBinding):
        return _decision(False, "binding is missing", {})
    if not isinstance(grant, RunGrant) or not grant.verify(binding, grant_key, at=at):
        return _decision(False, "run grant is invalid or expired", request)
    if not isinstance(request, Mapping) or frozenset(request) != _REQUEST_FIELDS:
        return _decision(False, "request fields are not allowed", request if isinstance(request, Mapping) else {})
    scope = {
        "plan_digest": binding.plan_digest,
        "session_id": binding.session_id,
        "nonce": binding.single_use_nonce,
        "provider": binding.provider,
        "model": binding.model,
        "model_version": binding.model_version,
        "role": binding.role,
        "operation": binding.operation,
    }
    for field, expected in scope.items():
        if request[field] != expected:
            return _decision(False, f"request {field} is outside the grant", request)
    for field, limit_name in (
        ("request_bytes", "max_input_bytes"),
        ("expected_output_bytes", "max_output_bytes"),
        ("turn", "max_turns"),
    ):
        value = request[field]
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value <= 0
            or value > binding.limits[limit_name]
        ):
            return _decision(False, f"request {field} exceeds the grant", request)
    if not isinstance(request["request_id"], str) or not request["request_id"]:
        return _decision(False, "request id is invalid", request)
    if not isinstance(request["prompt"], str):
        return _decision(False, "request prompt is invalid", request)
    try:
        replay_state.consume(
            nonce=grant.nonce,
            session_id=request["session_id"],
            request_id=request["request_id"],
            max_requests=int(binding.limits["max_requests"]),
        )
    except GatewayError as exc:
        return _decision(False, str(exc), request)
    return _decision(True, "request matches the run grant", request)


def _redact(value: Any, secrets: Tuple[str, ...]) -> Any:
    if isinstance(value, str):
        redacted = value
        for secret in secrets:
            if secret:
                redacted = redacted.replace(secret, "[REDACTED]")
        return redacted
    if isinstance(value, Mapping):
        return {str(key): _redact(item, secrets) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact(item, secrets) for item in value]
    return value


def _event(
    event_type: str,
    decision: GatewayDecision,
    binding: DockerGatewayBinding,
    details: Mapping[str, Any],
) -> GatewayAuditEvent:
    return GatewayAuditEvent(
        event_type=event_type,
        decision=decision.status,
        request_id=decision.request_id,
        session_id=decision.session_id,
        plan_digest=binding.plan_digest,
        provider=binding.provider,
        model_version=binding.model_version,
        role=binding.role,
        operation=binding.operation,
        details=MappingProxyType(dict(details)),
    )


def run_gateway(
    binding: DockerGatewayBinding,
    grant: RunGrant,
    request: Mapping[str, Any],
    replay_state: GatewayReplayState,
    *,
    provider_credential: str,
    upstream: Callable[[str, Mapping[str, str], Mapping[str, Any]], Mapping[str, Any]],
    grant_key: bytes,
    at: Optional[datetime] = None,
) -> GatewayResult:
    decision = authorize_gateway_request(
        binding,
        grant,
        request,
        replay_state,
        grant_key=grant_key,
        at=at,
    )
    prompt = request.get("prompt", "") if isinstance(request, Mapping) else ""
    prompt_digest = hashlib.sha256(str(prompt).encode("utf-8")).hexdigest()
    events = [
        _event(
            "authorization",
            decision,
            binding,
            {
                "reason": decision.reason,
                "prompt_digest": prompt_digest,
                "request_bytes": request.get("request_bytes") if isinstance(request, Mapping) else None,
            },
        )
    ]
    if not decision.allowed:
        return GatewayResult(
            decision=decision,
            response=MappingProxyType({"status": "BLOCKED_NOT_RUN"}),
            events=tuple(events),
        )
    if not isinstance(provider_credential, str) or not provider_credential:
        raise GatewayError("trusted provider credential is missing")

    body = {
        "model": binding.model,
        "model_version": binding.model_version,
        "input": request["prompt"],
        "max_output_bytes": request["expected_output_bytes"],
    }
    headers = {
        "authorization": f"Bearer {provider_credential}",
        "content-type": "application/json",
    }
    try:
        raw_response = upstream(_PROVIDER_ENDPOINT, headers, body)
    except Exception as exc:
        raise GatewayError(f"synthetic upstream failed: {type(exc).__name__}") from None
    if not isinstance(raw_response, Mapping):
        raise GatewayError("upstream response must be an object")
    if raw_response.get("model_version") != binding.model_version:
        raise GatewayError("upstream model snapshot differs from the grant")
    usage = raw_response.get("usage")
    if not isinstance(usage, Mapping):
        raise GatewayError("upstream response is missing usage")
    for field, limit_name in (
        ("input_bytes", "max_input_bytes"),
        ("output_bytes", "max_output_bytes"),
        ("cost_usd", "max_cost_usd"),
    ):
        value = usage.get(field)
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or value < 0
            or value > binding.limits[limit_name]
        ):
            raise GatewayError(f"upstream usage {field} exceeds the grant")

    sanitized = _redact(dict(raw_response), (provider_credential,))
    response_digest = hashlib.sha256(_canonical_json(sanitized)).hexdigest()
    events.append(
        _event(
            "upstream-response",
            decision,
            binding,
            {
                "response_digest": response_digest,
                "provider_session_id": sanitized.get("id"),
                "usage": dict(usage),
            },
        )
    )
    return GatewayResult(
        decision=decision,
        response=MappingProxyType(sanitized),
        events=tuple(events),
    )


def workload_gateway_environment(grant: RunGrant) -> Mapping[str, str]:
    if not isinstance(grant, RunGrant):
        raise GatewayError("RunGrant is required")
    return MappingProxyType(
        {
            "EVALUATE_RUN_GRANT": grant.to_token(),
            "PROVIDER_BASE_URL": _INTERNAL_BASE_URL,
        }
    )


def gateway_container_contract() -> Mapping[str, Any]:
    return MappingProxyType(
        {
            "user": "65532:65532",
            "ip_forwarding": False,
            "raw_socket": False,
            "network_admin": False,
            "workload_chosen_destination": False,
            "provider_endpoint": _PROVIDER_ENDPOINT,
        }
    )


def gateway_network_contract() -> Mapping[str, bool]:
    return MappingProxyType(
        {
            "internal": True,
            "workload_egress": False,
            "workload_dns": False,
            "ipv6": False,
            "gateway_egress": True,
        }
    )


def probe_codex_gateway_compatibility(
    adapter_config: Mapping[str, Any],
    synthetic_gateway: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> Mapping[str, Any]:
    required = {
        "provider": "openai",
        "adapter": "promptfoo-codex-sdk",
        "base_url": _INTERNAL_BASE_URL,
        "auth_scheme": "run-grant",
        "direct_egress": False,
    }
    if not isinstance(adapter_config, Mapping) or any(
        adapter_config.get(field) != expected for field, expected in required.items()
    ):
        return MappingProxyType(
            {"status": "BLOCKED_NOT_RUN", "model_executed": False}
        )
    try:
        response = synthetic_gateway(
            {"operation": "compatibility-probe", "model_executed": False}
        )
    except Exception:
        return MappingProxyType(
            {"status": "BLOCKED_NOT_RUN", "model_executed": False}
        )
    status = "READY_NOT_RUN" if response.get("synthetic") is True else "BLOCKED_NOT_RUN"
    return MappingProxyType({"status": status, "model_executed": False})


