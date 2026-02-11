import json
import os
import subprocess

LINT_RESULTS_PATH = r"c:\Dev\PyAgent\lint_results.json"
PYTHON_PATH = r"c:\Dev\PyAgent\.venv\Scripts\python.exe"

def run_ruff(file_path):
    try:
        res = subprocess.run([PYTHON_PATH, "-m", "ruff", "check", file_path], capture_output=True, text=True)
        return res.stdout, res.returncode
    except:
        return "", 0

def run_flake8(file_path):
    try:
        res = subprocess.run([PYTHON_PATH, "-m", "flake8", file_path, "--max-line-length=120"], capture_output=True, text=True)
        return res.stdout, res.returncode
    except:
        return "", 0

def main():
    if not os.path.exists(LINT_RESULTS_PATH):
        print("lint_results.json not found")
        return

    with open(LINT_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = []
    total_issues = 0
    original_count = len(data)

    for entry in data:
        file_path = entry["file"]
        if not os.path.exists(file_path):
            continue
            
        print(f"Syncing {file_path}...")
        ruff_out, ruff_rc = run_ruff(file_path)
        flake_out, flake_rc = run_flake8(file_path)
        
        entry["ruff"]["stdout"] = ruff_out
        entry["ruff"]["exit_code"] = ruff_rc
        entry["flake8"]["stdout"] = flake_out
        entry["flake8"]["exit_code"] = flake_rc
        
        # Count issues
        ruff_issues = len([l for l in ruff_out.splitlines() if l.strip() and "All checks passed!" not in l])
        flake_issues = len([l for l in flake_out.splitlines() if l.strip()])
        
        if ruff_issues == 0 and flake_issues == 0:
            # File is clean! Skip adding it back to the list
            print(f"  -> File {file_path} is now CLEAN. Removing.")
            continue
            
        total_issues += ruff_issues + flake_issues
        new_data.append(entry)

    with open(LINT_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

    print("\nSync Complete.")
    print(f"Original entries: {original_count}")
    print(f"Remaining entries: {len(new_data)}")
    print(f"Total remaining issues: {total_issues}")

if __name__ == "__main__":
    main()
