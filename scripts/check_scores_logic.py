import os
import subprocess
import sys

def run_pylint(file_path):
    pylint_cmd = [sys.executable, "-m", "pylint", file_path, "--reports=n", "--score=y"]
    try:
        result = subprocess.run(pylint_cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout
        for line in output.split("\n"):
            if "Your code has been rated at" in line:
                return line.strip()
        return "Score not found"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    base_dir = "src/core/base/logic"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = os.path.join(root, file)
                score = run_pylint(full_path)
                print(f"{full_path}: {score}")

if __name__ == "__main__":
    main()
