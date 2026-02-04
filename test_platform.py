import platform
import sys
print("Testing platform module...", flush=True)
try:
    s = platform.system()
    print(f"Platform: {s}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
print("Done.", flush=True)
