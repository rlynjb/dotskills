"""Strict, pinned provider capability inventory for Evaluate Skill v0.2."""

from __future__ import annotations

from dataclasses import dataclass
import json
import platform as host_platform
from pathlib import Path
import re
import shutil
import subprocess
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple


class InventoryError(ValueError):
    """The capability inventory is malformed or contains an unknown claim."""


_STATUSES = frozenset(("verified", "unverified", "unsupported"))
_BACKENDS = frozenset(("native", "docker"))
_PROFILES = frozenset(("no-tool", "read-only", "disposable-write", "mock-external"))
_TOOLS = ("promptfoo", "codex", "claude")
_VERSION_PATTERN = re.compile(r"(?<![0-9])([0-9]+\.[0-9]+\.[0-9]+)(?![0-9])")


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InventoryError(f"{name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise InventoryError(f"{name} field names must be strings")
    return value


def _exact_fields(value: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    actual = frozenset(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise InventoryError(f"{name} missing fields: {', '.join(missing)}")
    if unknown:
        raise InventoryError(f"{name} unknown fields: {', '.join(unknown)}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InventoryError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str) -> Tuple[str, ...]:
    if not isinstance(value, list):
        raise InventoryError(f"{name} must be an array")
    result = tuple(_text(item, f"{name} item") for item in value)
    if len(result) != len(set(result)):
        raise InventoryError(f"{name} must not contain duplicates")
    return result


@dataclass(frozen=True)
class CapabilityClaim:
    status: str
    required_probes: Tuple[str, ...]


@dataclass(frozen=True)
class ProviderDescriptor:
    provider_id: str
    provider_version: str
    adapter_id: str
    adapter_version: str


@dataclass(frozen=True)
class PlatformFingerprint:
    system: str
    release: str
    machine: str


@dataclass(frozen=True)
class CapabilityInventory:
    schema_version: str
    platform: PlatformFingerprint
    required_versions: Mapping[str, str]
    providers: Mapping[str, ProviderDescriptor]
    capabilities: Tuple[str, ...]
    claims: Mapping[Tuple[str, str, str, str], CapabilityClaim]

    def claims_for(
        self, provider: str, backend: str, profile: str
    ) -> Mapping[str, CapabilityClaim]:
        result = {
            capability: claim
            for (claim_provider, claim_backend, claim_profile, capability), claim in self.claims.items()
            if (claim_provider, claim_backend, claim_profile) == (provider, backend, profile)
        }
        return MappingProxyType(result)

    def claim(
        self, provider: str, backend: str, profile: str, capability: str
    ) -> CapabilityClaim:
        try:
            return self.claims[(provider, backend, profile, capability)]
        except KeyError:
            raise InventoryError(
                "unknown capability claim: "
                f"{provider}/{backend}/{profile}/{capability}"
            ) from None

    def provider_for_plan(self, provider_id: str, adapter_id: str) -> Optional[str]:
        matches = [
            name
            for name, descriptor in self.providers.items()
            if descriptor.provider_id == provider_id and descriptor.adapter_id == adapter_id
        ]
        if len(matches) != 1:
            return None
        return matches[0]

    def is_enforced(
        self,
        provider: str,
        backend: str,
        profile: str,
        capability: str,
        passed_probes: Tuple[str, ...] = (),
    ) -> bool:
        claim = self.claim(provider, backend, profile, capability)
        return claim.status == "verified" and set(claim.required_probes).issubset(
            passed_probes
        )


def _load_claim(value: Mapping[str, Any], name: str) -> CapabilityClaim:
    value = _mapping(value, name)
    _exact_fields(value, frozenset(("status", "required_probes")), name)
    status = _text(value["status"], f"{name}.status")
    if status not in _STATUSES:
        raise InventoryError(f"{name}.status is unknown: {status}")
    probes = _strings(value["required_probes"], f"{name}.required_probes")
    if status == "unverified" and not probes:
        raise InventoryError(f"{name} is unverified but has no required probes")
    return CapabilityClaim(status=status, required_probes=probes)


def _load_platform(value: Mapping[str, Any]) -> PlatformFingerprint:
    value = _mapping(value, "inventory.platform")
    _exact_fields(value, frozenset(("system", "release", "machine")), "inventory.platform")
    return PlatformFingerprint(
        system=_text(value["system"], "inventory.platform.system"),
        release=_text(value["release"], "inventory.platform.release"),
        machine=_text(value["machine"], "inventory.platform.machine"),
    )


def load_inventory(path: Path) -> CapabilityInventory:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InventoryError(f"cannot load capability inventory: {exc}") from None
    document = _mapping(document, "inventory")
    _exact_fields(
        document,
        frozenset(
            (
                "schema_version",
                "platform",
                "required_versions",
                "capabilities",
                "claim_sets",
                "providers",
            )
        ),
        "inventory",
    )

    capabilities = _strings(document["capabilities"], "inventory.capabilities")
    if not capabilities:
        raise InventoryError("inventory.capabilities must not be empty")
    known_capabilities = frozenset(capabilities)

    versions = _mapping(document["required_versions"], "inventory.required_versions")
    _exact_fields(versions, frozenset(_TOOLS), "inventory.required_versions")
    required_versions = {
        tool: _text(versions[tool], f"inventory.required_versions.{tool}")
        for tool in _TOOLS
    }

    raw_claim_sets = _mapping(document["claim_sets"], "inventory.claim_sets")
    if not raw_claim_sets:
        raise InventoryError("inventory.claim_sets must not be empty")
    claim_sets = {}
    for set_name, raw_claims in raw_claim_sets.items():
        set_name = _text(set_name, "inventory claim-set name")
        raw_claims = _mapping(raw_claims, f"inventory.claim_sets.{set_name}")
        _exact_fields(
            raw_claims,
            known_capabilities,
            f"inventory.claim_sets.{set_name}",
        )
        claim_sets[set_name] = {
            capability: _load_claim(
                raw_claims[capability],
                f"inventory.claim_sets.{set_name}.{capability}",
            )
            for capability in capabilities
        }

    raw_providers = _mapping(document["providers"], "inventory.providers")
    if not raw_providers:
        raise InventoryError("inventory.providers must not be empty")
    providers = {}
    claims = {}
    for provider_name, raw_provider in raw_providers.items():
        provider_name = _text(provider_name, "inventory provider name")
        raw_provider = _mapping(raw_provider, f"inventory.providers.{provider_name}")
        _exact_fields(
            raw_provider,
            frozenset(
                (
                    "provider_id",
                    "provider_version",
                    "adapter_id",
                    "adapter_version",
                    "backends",
                )
            ),
            f"inventory.providers.{provider_name}",
        )
        providers[provider_name] = ProviderDescriptor(
            provider_id=_text(
                raw_provider["provider_id"],
                f"inventory.providers.{provider_name}.provider_id",
            ),
            provider_version=_text(
                raw_provider["provider_version"],
                f"inventory.providers.{provider_name}.provider_version",
            ),
            adapter_id=_text(
                raw_provider["adapter_id"],
                f"inventory.providers.{provider_name}.adapter_id",
            ),
            adapter_version=_text(
                raw_provider["adapter_version"],
                f"inventory.providers.{provider_name}.adapter_version",
            ),
        )
        backends = _mapping(
            raw_provider["backends"], f"inventory.providers.{provider_name}.backends"
        )
        _exact_fields(
            backends,
            _BACKENDS,
            f"inventory.providers.{provider_name}.backends",
        )
        for backend in sorted(_BACKENDS):
            backend_value = _mapping(
                backends[backend],
                f"inventory.providers.{provider_name}.backends.{backend}",
            )
            _exact_fields(
                backend_value,
                frozenset(("profiles",)),
                f"inventory.providers.{provider_name}.backends.{backend}",
            )
            profiles = _mapping(
                backend_value["profiles"],
                f"inventory.providers.{provider_name}.backends.{backend}.profiles",
            )
            _exact_fields(
                profiles,
                _PROFILES,
                f"inventory.providers.{provider_name}.backends.{backend}.profiles",
            )
            for profile in sorted(_PROFILES):
                set_name = _text(
                    profiles[profile],
                    f"inventory.providers.{provider_name}.backends.{backend}.profiles.{profile}",
                )
                if set_name not in claim_sets:
                    raise InventoryError(f"unknown claim set: {set_name}")
                for capability, claim in claim_sets[set_name].items():
                    claims[(provider_name, backend, profile, capability)] = claim

    schema_version = _text(document["schema_version"], "inventory.schema_version")
    if schema_version != "0.2":
        raise InventoryError(f"unsupported inventory schema_version: {schema_version}")
    return CapabilityInventory(
        schema_version=schema_version,
        platform=_load_platform(document["platform"]),
        required_versions=MappingProxyType(required_versions),
        providers=MappingProxyType(providers),
        capabilities=capabilities,
        claims=MappingProxyType(claims),
    )


def inspect_platform_fingerprint() -> PlatformFingerprint:
    return PlatformFingerprint(
        system=host_platform.system().lower(),
        release=host_platform.release(),
        machine=host_platform.machine(),
    )


def inspect_installed_versions() -> dict[str, Optional[str]]:
    observed = {}
    for tool in _TOOLS:
        executable = shutil.which(tool)
        if not executable:
            observed[tool] = None
            continue
        try:
            result = subprocess.run(
                [executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
                shell=False,
            )
        except (OSError, subprocess.SubprocessError):
            observed[tool] = None
            continue
        output = f"{result.stdout}\n{result.stderr}"
        match = _VERSION_PATTERN.search(output) if result.returncode == 0 else None
        observed[tool] = match.group(1) if match else None
    return observed


def validate_installed_versions(
    inventory: CapabilityInventory, observed: Mapping[str, Optional[str]]
) -> list[str]:
    mismatches = []
    for tool in sorted(inventory.required_versions):
        required = inventory.required_versions[tool]
        actual = observed.get(tool)
        if actual is None:
            mismatches.append(f"{tool}: missing (required {required})")
        elif actual != required:
            mismatches.append(f"{tool}: observed {actual}, required {required}")
    return mismatches
