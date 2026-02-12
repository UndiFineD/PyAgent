import json
import os
import subprocess
import sys

def main():
    json_path = r"temp/lint_results.json"
    if not os.path.exists(json_path):
        print("No lint results found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Collect unique files that have errors
    files_to_fix = set()
    for entry in data:
        file_path = entry['file']
        # Normalize
        file_path = os.path.normpath(file_path)
        if os.path.exists(file_path):
            files_to_fix.add(file_path)

    print(f"Found {len(files_to_fix)} files to process with autopep8.")

    count = 0
    for f in files_to_fix:
        # python -m autopep8 --in-place --max-line-length 120 --aggressive <file>
        cmd = [
            sys.executable, "-m", "autopep8",
            "--in-place",
            "--max-line-length", "120",
            "--aggressive",
            f
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Processed: {f}")
            count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error processing {f}: {e.stderr.decode()}")
        except Exception as e:
            print(f"Failed {f}: {e}")

    print(f"Finished processing {count} files.")

if __name__ == "__main__":
    main()
