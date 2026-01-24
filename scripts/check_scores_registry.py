import os
import subprocess

def run_pylint(file_path):
    pylint_cmd = [
        "C:/DEV/PyAgent/.venv/Scripts/python.exe",
        "-m", "pylint",
        file_path
    ]
    try:
        result = subprocess.run(pylint_cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout
        # Extract score
        for line in output.split('\n'):
            if "Your code has been rated at" in line:
                return line.strip()
        return "Score not found"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    files = [
        r"c:\DEV\PyAgent\src\core\base\registry\agent_registry.py",
        r"c:\DEV\PyAgent\src\core\base\registry\architecture_mapper.py",
        r"c:\DEV\PyAgent\src\core\base\registry\extension_registry.py",
        r"c:\DEV\PyAgent\src\core\base\registry\module_loader.py",
    ]
    for f in files:
        score = run_pylint(f)
        print(f"{os.path.basename(f)}: {score}")
