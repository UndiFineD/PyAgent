import json
import subprocess
import sys
import os

LINT_RESULTS = r"temp/lint_results.json"
CLEANUP_SCRIPT = r"tools/cleanup_whitespace.py"

if not os.path.exists(LINT_RESULTS):
    print(f"Error: {LINT_RESULTS} not found")
    sys.exit(1)

with open(LINT_RESULTS, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for entry in data:
    file_path = entry["file"]
    if os.path.exists(file_path):
        subprocess.run([sys.executable, CLEANUP_SCRIPT, file_path])
        count += 1

print(f"Ran whitespace cleanup on {count} files.")
