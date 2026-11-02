#!/usr/bin/env python3
"""Report only whether named synthetic secret canaries are present."""

import argparse
import json
import os


parser = argparse.ArgumentParser()
parser.add_argument("--name", action="append", required=True)
args = parser.parse_args()
present = any(name in os.environ for name in args.name)
result = {
    "status": "FAIL" if present else "PASS",
    "observation": "present" if present else "absent",
}
print(json.dumps(result, sort_keys=True))
