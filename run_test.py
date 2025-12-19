import subprocess
import sys

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

if __name__ == "__main__":
    # Run agent on test_e2e.py
    # We need to be careful with paths.
    # Assuming we are in repo root.
    cmd = "python src/agent.py --dir . --dry-run --strategy cot --only-agents coder --verbose normal"
    print(f"Running: {cmd}")
    run_command(cmd)
