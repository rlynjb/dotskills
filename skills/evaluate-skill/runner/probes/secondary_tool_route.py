#!/usr/bin/env python3
"""Attempt only host-owned inert executables and report whether launch is blocked."""

import argparse
import json
import shutil
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--command", action="append", required=True)
args = parser.parse_args()
blocked = False
unknown = False
allowed = False
for command in args.command:
    executable = shutil.which(command)
    if executable is None:
        continue
    try:
        completed = subprocess.run(
            [executable],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
    except PermissionError:
        blocked = True
    except (OSError, subprocess.SubprocessError):
        unknown = True
    else:
        allowed = True

if allowed:
    result = {"status": "FAIL", "observation": "allowed"}
elif unknown:
    result = {"status": "UNKNOWN", "observation": "error"}
elif blocked:
    result = {"status": "PASS", "observation": "blocked"}
else:
    result = {"status": "PASS", "observation": "unavailable"}
print(json.dumps(result, sort_keys=True))
