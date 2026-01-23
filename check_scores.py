import subprocess
import sys

files = [
    "c:/DEV/PyAgent/src/core/base/execution/agent_command_handler.py",
    "c:/DEV/PyAgent/src/core/base/execution/agent_delegator.py",
    "c:/DEV/PyAgent/src/core/base/execution/shell_executor.py"
]

for f in files:
    print(f"Checking {f}...")
    result = subprocess.run([sys.executable, "-m", "pylint", f], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Your code has been rated at" in line:
            print(line)
