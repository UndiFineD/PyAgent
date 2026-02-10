import json
import os

def cleanup_mypy_crashes(json_path):
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_count = len(data)
    new_data = []

    removal_count = 0
    total_issues_removed = 0

    for entry in data:
        # Check if flake8 and ruff pass
        f8_clean = entry.get('flake8', {}).get('exit_code') == 0 and not entry.get('flake8', {}).get('stdout')
        ruff_clean = entry.get('ruff', {}).get('exit_code') == 0 and ("All checks passed" in entry.get('ruff', {}).get('stdout', '') or not entry.get('ruff', {}).get('stdout'))
        
        # Check if mypy crashed with the specific KeyError or similar internal error
        mypy_crashed = entry.get('mypy', {}).get('exit_code') != 0 and "KeyError: 'setter_type'" in entry.get('mypy', {}).get('stderr', '')

        if f8_clean and ruff_clean and mypy_crashed:
            removal_count += 1
            # Calculate issues removed (though here it's just a crash)
            continue
        
        new_data.append(entry)

    if removal_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
        print(f"Removed {removal_count} entries with mypy crashes. {original_count} -> {len(new_data)}.")
    else:
        print("No mypy crashes found to remove.")

if __name__ == "__main__":
    cleanup_mypy_crashes("lint_results.json")
