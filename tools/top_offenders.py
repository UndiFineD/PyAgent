import json
import os

LINT_RESULTS_PATH = r"c:\Dev\PyAgent\lint_results.json"

def main():
    if not os.path.exists(LINT_RESULTS_PATH):
        print("Not found")
        return

    with open(LINT_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_issues = []
    for entry in data:
        issues = 0
        if "flake8" in entry and entry["flake8"]["stdout"]:
            issues += len(entry["flake8"]["stdout"].splitlines())
        if "ruff" in entry and entry["ruff"]["stdout"]:
            # Ruff output is more complex, but we can count lines starting with it
            issues += len([l for l in entry["ruff"]["stdout"].splitlines() if l.strip()])
        
        file_issues.append((entry["file"], issues))

    file_issues.sort(key=lambda x: x[1], reverse=True)

    print(f"Top 20 Offending Files (out of {len(data)}):")
    for f, count in file_issues[:20]:
        print(f"{count:4} : {f}")

if __name__ == "__main__":
    main()
