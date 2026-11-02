"""Strict immutable Docker v0.4 execution, gateway, and evidence bindings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import re
from types import MappingProxyType
from typing import Any, Mapping


class DockerContractError(ValueError):
    """A Docker boundary binding is incomplete, mutable, or malformed."""


_SCHEMA_VERSION = "0.4"
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_PATTERN = re.compile(
    r"^[a-z0-9][a-z0-9._/-]*@sha256:([0-9a-f]{64})$"
)
_ROLES = frozenset(("with-skill", "without-skill", "judge"))
_PROFILES = frozenset(("read-only",))
_MAX_GRANT_TTL = timedelta(hours=2)
_LIMIT_FIELDS = frozenset(
    (
        "max_sessions",
        "max_requests",
        "max_turns",
        "max_input_bytes",
        "max_output_bytes",
        "max_cost_usd",
    )
)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerContractError(f"{name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise DockerContractError(f"{name} field names must be strings")
    return value


def _exact_fields(value: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    actual = frozenset(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise DockerContractError(f"{name} missing fields: {', '.join(missing)}")
    if unknown:
        raise DockerContractError(f"{name} unknown fields: {', '.join(unknown)}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DockerContractError(f"{name} must be a non-empty canonical string")
    return value


def _schema(value: Any, name: str) -> str:
    schema_version = _text(value, name)
    if schema_version != _SCHEMA_VERSION:
        raise DockerContractError(f"{name} must be {_SCHEMA_VERSION}")
    return schema_version


def _digest(value: Any, name: str) -> str:
    digest = _text(value, name)
    if not _SHA256_PATTERN.fullmatch(digest):
        raise DockerContractError(
            f"{name} must be 64 lowercase hexadecimal characters"
        )
    return digest


def _image(value: Any, name: str) -> tuple[str, str]:
    reference = _text(value, name)
    match = _IMAGE_PATTERN.fullmatch(reference)
    if match is None:
        raise DockerContractError(
            f"{name} must be an immutable name@sha256:<digest> reference"
        )
    return reference, match.group(1)


def _timestamp(value: Any, name: str) -> datetime:
    text = _text(value, name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise DockerContractError(f"{name} must be an ISO-8601 timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise DockerContractError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _canonical_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class DockerExecutionBinding:
    schema_version: str
    plan_digest: str
    provider: str
    profile: str
    workload_image: str
    workload_image_digest: str
    gateway_image: str
    gateway_image_digest: str
    build_input_digest: str
    runtime_inventory_digest: str
    launch_policy_digest: str
    network_policy_digest: str
    seccomp_policy_digest: str
    gateway_policy_digest: str
    observer_policy_digest: str
    fixture_digest: str
    cleanup_policy_digest: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerExecutionBinding":
        value = _mapping(value, "docker execution binding")
        fields = frozenset(cls.__dataclass_fields__)
        _exact_fields(value, fields, "docker execution binding")
        workload_image, workload_reference_digest = _image(
            value["workload_image"], "docker execution binding.workload_image"
        )
        gateway_image, gateway_reference_digest = _image(
            value["gateway_image"], "docker execution binding.gateway_image"
        )
        workload_digest = _digest(
            value["workload_image_digest"],
            "docker execution binding.workload_image_digest",
        )
        gateway_digest = _digest(
            value["gateway_image_digest"],
            "docker execution binding.gateway_image_digest",
        )
        if workload_reference_digest != workload_digest:
            raise DockerContractError(
                "docker execution binding workload image digest mismatch"
            )
        if gateway_reference_digest != gateway_digest:
            raise DockerContractError(
                "docker execution binding gateway image digest mismatch"
            )
        profile = _text(value["profile"], "docker execution binding.profile")
        if profile not in _PROFILES:
            raise DockerContractError(
                f"docker execution binding profile is unsupported: {profile}"
            )
        digest_fields = {
            name: _digest(value[name], f"docker execution binding.{name}")
            for name in fields
            if name.endswith("_digest")
            and name not in ("workload_image_digest", "gateway_image_digest")
        }
        return cls(
            schema_version=_schema(
                value["schema_version"], "docker execution binding.schema_version"
            ),
            plan_digest=digest_fields.pop("plan_digest"),
            provider=_text(value["provider"], "docker execution binding.provider"),
            profile=profile,
            workload_image=workload_image,
            workload_image_digest=workload_digest,
            gateway_image=gateway_image,
            gateway_image_digest=gateway_digest,
            **digest_fields,
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name in self.__dataclass_fields__
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


@dataclass(frozen=True)
class DockerGatewayBinding:
    schema_version: str
    plan_digest: str
    provider: str
    provider_version: str
    adapter: str
    adapter_version: str
    model: str
    model_version: str
    role: str
    operation: str
    limits: Mapping[str, float]
    issued_at: str
    expires_at: str
    single_use_nonce: str
    session_id: str
    gateway_policy_digest: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerGatewayBinding":
        value = _mapping(value, "docker gateway binding")
        _exact_fields(
            value, frozenset(cls.__dataclass_fields__), "docker gateway binding"
        )
        role = _text(value["role"], "docker gateway binding.role")
        if role not in _ROLES:
            raise DockerContractError(f"docker gateway binding role is unsupported: {role}")
        limits = _mapping(value["limits"], "docker gateway binding.limits")
        _exact_fields(limits, _LIMIT_FIELDS, "docker gateway binding.limits")
        normalized_limits: dict[str, float] = {}
        for name in sorted(_LIMIT_FIELDS):
            limit = limits[name]
            if (
                isinstance(limit, bool)
                or not isinstance(limit, (int, float))
                or not math.isfinite(limit)
                or limit <= 0
            ):
                raise DockerContractError(
                    f"docker gateway binding.limits.{name} must be positive"
                )
            if name != "max_cost_usd" and not float(limit).is_integer():
                raise DockerContractError(
                    f"docker gateway binding.limits.{name} must be a whole number"
                )
            normalized_limits[name] = limit
        issued_at = _text(value["issued_at"], "docker gateway binding.issued_at")
        expires_at = _text(value["expires_at"], "docker gateway binding.expires_at")
        issued = _timestamp(issued_at, "docker gateway binding.issued_at")
        expires = _timestamp(expires_at, "docker gateway binding.expires_at")
        if issued >= expires:
            raise DockerContractError(
                "docker gateway binding expires_at must be later than issued_at"
            )
        if expires - issued > _MAX_GRANT_TTL:
            raise DockerContractError(
                "docker gateway binding validity window must not exceed two hours"
            )
        return cls(
            schema_version=_schema(
                value["schema_version"], "docker gateway binding.schema_version"
            ),
            plan_digest=_digest(
                value["plan_digest"], "docker gateway binding.plan_digest"
            ),
            provider=_text(value["provider"], "docker gateway binding.provider"),
            provider_version=_text(
                value["provider_version"], "docker gateway binding.provider_version"
            ),
            adapter=_text(value["adapter"], "docker gateway binding.adapter"),
            adapter_version=_text(
                value["adapter_version"], "docker gateway binding.adapter_version"
            ),
            model=_text(value["model"], "docker gateway binding.model"),
            model_version=_text(
                value["model_version"], "docker gateway binding.model_version"
            ),
            role=role,
            operation=_text(value["operation"], "docker gateway binding.operation"),
            limits=MappingProxyType(normalized_limits),
            issued_at=issued_at,
            expires_at=expires_at,
            single_use_nonce=_text(
                value["single_use_nonce"],
                "docker gateway binding.single_use_nonce",
            ),
            session_id=_text(
                value["session_id"], "docker gateway binding.session_id"
            ),
            gateway_policy_digest=_digest(
                value["gateway_policy_digest"],
                "docker gateway binding.gateway_policy_digest",
            ),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "plan_digest": self.plan_digest,
            "provider": self.provider,
            "provider_version": self.provider_version,
            "adapter": self.adapter,
            "adapter_version": self.adapter_version,
            "model": self.model,
            "model_version": self.model_version,
            "role": self.role,
            "operation": self.operation,
            "limits": dict(self.limits),
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "single_use_nonce": self.single_use_nonce,
            "session_id": self.session_id,
            "gateway_policy_digest": self.gateway_policy_digest,
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


@dataclass(frozen=True)
class DockerEvidenceBinding:
    schema_version: str
    plan_digest: str
    run_nonce: str
    execution_binding_digest: str
    launch_digest: str
    gateway_digest: str
    observer_digest: str
    state_digest: str
    cleanup_digest: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerEvidenceBinding":
        value = _mapping(value, "docker evidence binding")
        fields = frozenset(cls.__dataclass_fields__)
        _exact_fields(value, fields, "docker evidence binding")
        digests = {
            name: _digest(value[name], f"docker evidence binding.{name}")
            for name in fields
            if name.endswith("_digest")
        }
        return cls(
            schema_version=_schema(
                value["schema_version"], "docker evidence binding.schema_version"
            ),
            plan_digest=digests.pop("plan_digest"),
            run_nonce=_text(value["run_nonce"], "docker evidence binding.run_nonce"),
            **digests,
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name in self.__dataclass_fields__
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())
