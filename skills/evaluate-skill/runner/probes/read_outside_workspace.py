#!/usr/bin/env python3
"""Report whether a host-owned outside-workspace read canary is denied."""

import argparse
import json
import os


parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True)
args = parser.parse_args()
try:
    descriptor = os.open(args.path, os.O_RDONLY)
except PermissionError:
    result = {"status": "PASS", "observation": "denied"}
except OSError:
    result = {"status": "UNKNOWN", "observation": "error"}
else:
    os.close(descriptor)
    result = {"status": "FAIL", "observation": "allowed"}
print(json.dumps(result, sort_keys=True))
