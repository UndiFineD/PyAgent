import os
import subprocess
import json
import re

def main():
    # Run ruff to get F401 errors in JSON format
    try:
        ruff_path = r"C:\DEV\PyAgent\.venv\Scripts\ruff.exe"
        result = subprocess.run(
            [ruff_path, "check", "src/", "--select=F401", "--output-format", "json"],
            capture_output=True,
            text=True,
            check=False
        )
        if not result.stdout:
            print("No F401 errors found.")
            return
            
        errors = json.loads(result.stdout)
    except Exception as e:
        print(f"Error running ruff: {e}")
        return

    # Filter for __init__.py files
    init_errors = [e for e in errors if e['filename'].endswith('__init__.py')]
    
    # Process each file once
    files_to_fix = {}
    for e in init_errors:
        filename = e['filename']
        if filename not in files_to_fix:
            files_to_fix[filename] = []
        files_to_fix[filename].append(e)

    for filename, file_errors in files_to_fix.items():
        print(f"Fixing {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        lines = content.splitlines(keepends=True)

        # Sort errors by line number descending and column descending
        # to apply changes from bottom-up/right-to-left
        sorted_errors = sorted(file_errors, key=lambda x: (x['location']['row'], x['location']['column']), reverse=True)

        for e in sorted_errors:
            line_idx = e['location']['row'] - 1
            col_start = e['location']['column']
            col_end = e['end_location']['column']
            
            # Simple check if the line index is valid
            if line_idx >= len(lines):
                continue
                
            line = lines[line_idx]
            
            # Extract the actual symbol from the message
            # Typical F401 message: "`.DependencyContainer.DependencyContainer` imported but unused"
            # Or "`.swarm.OrchestratorAgent.OrchestratorAgent` imported but unused"
            # We want the last segment of the part in backticks.
            msg = e['message']
            match = re.search(r"`([^`]+)`", msg)
            if not match:
                continue
            
            full_ref = match.group(1)
            symbol = full_ref.split('.')[-1]
            
            # We use the column information to be precise
            # col_start and col_end are 1-based
            start_pos = col_start - 1
            end_pos = col_end - 1
            
            actual_text = line[start_pos:end_pos]
            
            # If the actual text is our symbol (or part of it if it's aliased already but not as intended)
            # we replace it with "symbol as symbol"
            if symbol == actual_text and f"as {symbol}" not in line:
                 lines[line_idx] = line[:start_pos] + f"{symbol} as {symbol}" + line[end_pos:]
            elif actual_text.strip() == symbol:
                 # Handle cases where there might be some whitespace in the column range
                 prefix_len = len(actual_text) - len(actual_text.lstrip())
                 suffix_len = len(actual_text) - len(actual_text.rstrip())
                 lines[line_idx] = line[:start_pos + prefix_len] + f"{symbol} as {symbol}" + line[end_pos - suffix_len:]


        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

if __name__ == "__main__":
    main()
