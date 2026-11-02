#!/opt/evaluate/bin/python3
"""Fixed gateway container entrypoint; network policy is supplied by the host."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Sequence


class GatewayEntrypointError(ValueError):
    pass


_BINDING = Path("/run/evaluate/gateway-binding.json")
_LEDGER = Path("/var/lib/evaluate-gateway/replay")


def parse_invocation(argv: Sequence[str]) -> tuple[Path, Path]:
    if tuple(argv) != (
        "serve",
        "--binding",
        str(_BINDING),
        "--replay-ledger",
        str(_LEDGER),
    ):
        raise GatewayEntrypointError("gateway invocation must use fixed binding and ledger paths")
    return _BINDING, _LEDGER


def main(argv: Sequence[str] | None = None) -> int:
    try:
        binding, ledger = parse_invocation(sys.argv[1:] if argv is None else argv)
    except GatewayEntrypointError as exc:
        print(json.dumps({"status": "BLOCKED_NOT_RUN", "reason": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": "GATEWAY_CONTRACT_READY_NOT_RUN",
                "binding": str(binding),
                "ledger": str(ledger),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
