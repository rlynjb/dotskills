#!/usr/bin/env python3
"""Report whether a host-owned network canary connection is denied."""

import argparse
import json
import socket


parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True)
parser.add_argument("--port", required=True, type=int)
args = parser.parse_args()
try:
    connection = socket.create_connection((args.host, args.port), timeout=1)
except PermissionError:
    result = {"status": "PASS", "observation": "denied"}
except OSError:
    result = {"status": "UNKNOWN", "observation": "error"}
else:
    connection.close()
    result = {"status": "FAIL", "observation": "allowed"}
print(json.dumps(result, sort_keys=True))
