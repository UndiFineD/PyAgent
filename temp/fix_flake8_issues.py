
import os
import re
import subprocess
from pathlib import Path

FLAKE8_LOG = r"c:\DEV\PyAgent\docs\work\flake8_clean.txt"
WS_ROOT = Path(r"c:\DEV\PyAgent")



def run_cmd(cmd, cwd=WS_ROOT):

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result

def parse_flake8_log():









    file_issues = {}
    if not os.path.exists(FLAKE8_LOG):
        print(f"Log not found: {FLAKE8_LOG}")
        return {}

    # Comprehensive ANSI stripper
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


    print(f"Opening log file: {FLAKE8_LOG}")
    lines_parsed = 0
    lines_failed = 0
    with open(FLAKE8_LOG, "r", encoding="utf-8", errors="ignore") as f:






        for line in f:
            # Strip ANSI codes immediately
            line = ansi_escape.sub('', line).strip()
            if not line: continue

            # Standard flake8 format: path:line:col: CODE message
            # But sometimes we have ./path or path


            match = re.match(r"^(.+?):(\d+):(\d+):\s*([A-Z0-9]+)\s+(.*)$", line)
            if match:
                file_rel, line_num, col, code, message = match.groups()
                lines_parsed += 1

                file_rel = file_rel.replace("/", "\\")






                if file_rel.startswith(".\\"):
                    file_rel = file_rel[2:]

                if file_rel not in file_issues:
                    file_issues[file_rel] = []

                file_issues[file_rel].append({
                    "line": int(line_num),
                    "col": int(col),
                    "code": code,
                    "message": message
                })


            else:


                lines_failed += 1


    print(f"Parsed {lines_parsed} lines, failed to parse {lines_failed} lines.")

    return file_issues






def fix_unsed_import(lines, line_num, code, message):
    idx = line_num - 1
    if idx < 0 or idx >= len(lines): return False
    line = lines[idx]
    if line is None: return False

    match = re.search(r"'([^']+)' imported but unused", message)
    if not match: return False
    pkg = match.group(1)

    strip_line = line.strip()


    if re.fullmatch(rf"import {re.escape(pkg)}", strip_line):




        lines[idx] = None
        return True


    if re.fullmatch(rf"from [\w\.]+ import {re.escape(pkg)}", strip_line):
        lines[idx] = None
        return True


    return False


def main():
    file_issues = parse_flake8_log()




    files = sorted(list(file_issues.keys()))
    print(f"Found {len(files)} files with issues.")

    processed = 0
    for file_rel in files:
        file_path = WS_ROOT / file_rel
        if not file_path.exists(): continue

        print(f"[{processed+1}] Fixing {file_rel}...")



        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception: continue


        lines = content.splitlines()
        # Process files from bottom to top to preserve line indices
        issues = sorted(file_issues[file_rel], key=lambda x: x['line'], reverse=True)
        fixed_count = 0

        for issue in issues:
            line_num = issue['line']
            code = issue['code']


            idx = line_num - 1
            if idx < 0 or idx >= len(lines): continue

            line = lines[idx]


            if line is None: continue

            if code == "W293": # blank line contains whitespace
                if line.isspace():
                    lines[idx] = ""




                    fixed_count += 1
            elif code == "W291": # trailing whitespace
                lines[idx] = line.rstrip()


                fixed_count += 1
            elif code == "F401":  # unused import
                if fix_unsed_import(lines, line_num, code, issue['message']):
                    fixed_count += 1
            elif code in ["E301", "E302", "E305"]:
                needed = 1 if code == "E301" else 2
                existing = 0
                check_idx = idx - 1
                while check_idx >= 0:
                    if lines[check_idx] is not None and lines[check_idx].strip() == "":

                        existing += 1
                        check_idx -= 1
                    else: break
                to_add = needed - existing


                for _ in range(to_add):
                    lines.insert(idx, "")
                    fixed_count += 1
            elif code == "E303":  # too many blank lines
                # Start scanning from one line above the trigger point
                t = idx - 1
                while t >= 0 and lines[t] is not None and lines[t].strip() == "":
                    lines[t] = None
                    fixed_count += 1
                    t -= 1
            elif code == "E261": # at least two spaces before inline comment




                if "  #" in line and not line.startswith("#"):
                    parts = line.split("  #", 1)
                    if not parts[0].endswith("  "):






                        lines[idx] = parts[0].rstrip() + "  #" + parts[1]
                        fixed_count += 1
            elif code == "E111":  # indentation is not a multiple of four
                # Only fix if it's spaces and we can just fix it
                if line.startswith(" "):
                    indent = len(line) - len(line.lstrip())
                    if indent % 4 != 0:
                        new_indent = round(indent / 4) * 4
                        lines[idx] = (" " * new_indent) + line.lstrip()
                        fixed_count += 1

        lines = [l for l in lines if l is not None]
        new_content = "\n".join(lines).rstrip() + "\n"
        if new_content == "\n": new_content = ""

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            check = run_cmd(f"python -m py_compile {file_rel}")
            if check.returncode != 0:
                print(f"  !!! Syntax error, reverting {file_rel}")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                print(f"  Fixed {fixed_count} issues.")

        processed += 1

    print("Done.")



if __name__ == "__main__":
    main()
