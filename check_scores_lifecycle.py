import subprocess
import sys

files = [
    "c:/DEV/PyAgent/src/core/base/lifecycle/agent_core.py",
    "c:/DEV/PyAgent/src/core/base/lifecycle/agent_update_manager.py",
    "c:/DEV/PyAgent/src/core/base/lifecycle/base_agent.py",
    "c:/DEV/PyAgent/src/core/base/lifecycle/base_agent_core.py",
    "c:/DEV/PyAgent/src/core/base/lifecycle/graceful_shutdown.py",
    "c:/DEV/PyAgent/src/core/base/lifecycle/version.py"
]

for f in files:
    print(f"Checking {f}...")
    result = subprocess.run([sys.executable, "-m", "pylint", f], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Your code has been rated at" in line:
            print(line)
