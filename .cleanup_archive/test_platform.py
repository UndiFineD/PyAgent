#!/usr/bin/env python3

import platform
from typing import cast

print("Testing platform module...", flush=True)
try:
    s: str = cast(str, platform.system())
    print(f"Platform: {s}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
print("Done.", flush=True)
