#!/usr/bin/env python3
"""Report only whether forbidden secondary command routes are discoverable."""

import argparse
import json
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("--command", action="append", required=True)
args = parser.parse_args()
available = any(shutil.which(command) for command in args.command)
result = {
    "status": "FAIL" if available else "PASS",
    "observation": "available" if available else "unavailable",
}
print(json.dumps(result, sort_keys=True))
