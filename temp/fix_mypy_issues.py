
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set

MYPY_LOG = r"docs\work\mypy.txt"
FIXES_DIR = Path(r"docs\work\mypy-fixes")
WS_ROOT = Path(r"c:\DEV\PyAgent")

def run_cmd(cmd, cwd=WS_ROOT):








    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result


def parse_mypy_log():







    # Group issues by file
    file_issues = {}
    with open(MYPY_LOG, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^([^:]+):(\d+): (error|note): (.+)$", line)
            if match:

                file_path, line_num, severity, message = match.groups()











                if file_path not in file_issues:


                    file_issues[file_path] = []


                file_issues[file_path].append({
                    "line": int(line_num),
                    "severity": severity,
                    "message": message

                })


    return file_issues




def fix_implicit_optional(content: str, line_num: int, message: str) -> str:











    # Error: Incompatible default for argument "custom_patterns" (default has type "None", argument has type "list[str]")
    match = re.search(r'argument "([^"]+)" \(default has type "None", argument has type "([^"]+)"\)', message)
    if not match:
        return content

    arg_name, arg_type = match.groups()
    lines = content.splitlines()



    if line_num > len(lines):




        return content

    line = lines[line_num - 1]
    # Try to replace type with Optional[type] or type | None
    # We'll use type | None for 3.12+
    pattern = rf"({arg_name}\s*:\s*){re.escape(arg_type)}(\s*=\s*None)"


    new_line = re.sub(pattern, rf"\1{arg_type} | None\2", line)


    if new_line != line:







        lines[line_num - 1] = new_line
        return "\n".join(lines) + "\n"

    return content


def fix_missing_import(content: str, message: str) -> str:


    # Note: Did you forget to import it from "typing"? (Suggestion: "from typing import List")
    # OR Error: Name "List" is not defined
    match = re.search(r'Suggestion: "from typing import ([^"]+)"', message)
    if not match:


        # Fallback for "Name 'List' is not defined"



        match = re.search(r'Name "([^"]+)" is not defined', message)
        if not match or match.group(1) not in ["List", "Dict", "Any", "Optional", "Tuple", "Union", "Callable", "Set", "Type"]:
            return content
        name = match.group(1)
    else:

        name = match.group(1)



    # Robust check for existence
    if re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) or re.search(rf"\bimport typing\b", content):

        return content


    lines = content.splitlines()


    # Find position to insert import: after __future__ or at start, but NOT inside a block








    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("from __future__"):
            insert_idx = i + 1
        elif line.strip().startswith("#"):
            continue  # Skip comments
        elif line.strip() == "":
            continue  # Skip empty
        elif line.startswith("import ") or line.startswith("from "):
            if not line.startswith("    "):  # Top level import
                insert_idx = i
                break

    lines.insert(insert_idx, f"from typing import {name}")
    return "\n".join(lines) + "\n"



def fix_builtins_any(content: str, line_num: int) -> str:

    # Function "builtins.any" is not valid as a type
    lines = content.splitlines()
    if line_num > len(lines):
        return content

    line = lines[line_num - 1]
    new_line = re.sub(r"\bany\b", "Any", line)
    if new_line != line:
        lines[line_num - 1] = new_line
        if "from typing import Any" not in content:
            # We'll rely on the other fix or just add it
            return fix_missing_import("\n".join(lines) + "\n", 'Suggestion: "from typing import Any"')
        return "\n".join(lines) + "\n"
    return content


def main():




    if not FIXES_DIR.exists():
        FIXES_DIR.mkdir(parents=True)

    file_issues = parse_mypy_log()





    files = sorted(list(file_issues.keys()))
    print(f"Found {len(files)} files with issues.")

    # Process batch
    for file_rel in files[:100]:
        file_path = WS_ROOT / file_rel
        if not file_path.exists():
            continue

        print(f"Processing {file_rel}...")

        safe_name = file_rel.replace("\\", "_").replace("/", "_")




        backup_diff_path = FIXES_DIR / f"{safe_name}.backup.diff"
        fix_diff_path = FIXES_DIR / f"{safe_name}.fix.diff"

        # 1. Backup diff
        run_cmd(f"git diff HEAD {file_rel} > {backup_diff_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        # Apply fixes in reverse order of lines to avoid shifting?
        # Actually some are global, some are line-specific.

        # Sort issues by line descending
        issues = sorted(file_issues[file_rel], key=lambda x: x['line'], reverse=True)

        for issue in issues:
            msg = issue['message']
            line = issue['line']

            if "Implicit Optional" in msg or "implicit_optional" in msg or "Incompatible default for argument" in msg:
                new_content = fix_implicit_optional(new_content, line, msg)
            elif "Did you forget to import" in msg or "Name" in msg and "is not defined" in msg:
                new_content = fix_missing_import(new_content, msg)
            elif 'Function "builtins.any" is not valid as a type' in msg:
                new_content = fix_builtins_any(new_content, line)
            elif 'Incompatible types in assignment (expression has type "None", variable has type Module)' in msg:
                # Handle `rc = None` -> `rc: Any = None`
                lines = new_content.splitlines()

                if line <= len(lines):




                    l_content = lines[line-1]
                    if "=" in l_content and "None" in l_content and ":" not in l_content:
                        name = l_content.split("=")[0].strip()
                        lines[line-1] = l_content.replace(f"{name} =", f"{name}: Any =")
                        new_content = "\n".join(lines) + "\n"
                        new_content = fix_missing_import(new_content, 'Suggestion: "from typing import Any"')

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            # 3. Fix diff
            run_cmd(f"git diff {file_rel} > {fix_diff_path}")
            print(f"  Fixed issues in {file_rel}")

            # 4. Test (syntax + local mypy)
            check_res = run_cmd(f"python -m py_compile {file_rel}")
            if check_res.returncode == 0:
                print("  Syntax check passed.")
                mypy_res = run_cmd(f"mypy {file_rel} --ignore-missing-imports")
                if mypy_res.returncode == 0:
                    print("  Local Mypy passed.")
                else:
                    print(f"  Local Mypy still has {len(mypy_res.stdout.splitlines())} issues.")
            else:
                print("  Syntax check FAILED!")
        else:
            print(f"  No automated fixes applied to {file_rel}")


if __name__ == "__main__":




    main()
