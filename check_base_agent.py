import os
import subprocess

def run_pylint(file_path):
    pylint_cmd = [
        "C:/DEV/PyAgent/.venv/Scripts/python.exe",
        "-m", "pylint",
        file_path
    ]
    result = subprocess.run(pylint_cmd, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    file_to_check = r"c:\DEV\PyAgent\src\core\base\lifecycle\base_agent.py"
    output = run_pylint(file_to_check)
    with open("final_score.txt", "w") as f:
        f.write(output)
    print("Done")
