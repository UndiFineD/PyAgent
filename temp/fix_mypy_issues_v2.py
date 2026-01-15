
import os
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
    file_issues = {}
    if not os.path.exists(MYPY_LOG):
        return {}
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



def fix_missing_import(content: str, message: str) -> str:










    match = re.search(r'Suggestion: "from typing import ([^"]+)"', message)
    if not match:
        match = re.search(r'Name "([^"]+)" is not defined', message)
        if not match or match.group(1) not in ["List", "Dict", "Any", "Optional", "Tuple", "Union", "Callable", "Set", "Type", "Iterable"]:
            return content




        name = match.group(1)
    else:
        name = match.group(1)

    if re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) or re.search(rf"\bimport typing\b", content):



        return content

    lines = content.splitlines()

    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("from __future__"):
            insert_idx = i + 1


        elif line.strip().startswith("#"):
            continue
        elif line.strip() == "":
            continue
        elif (line.startswith("import ") or line.startswith("from ")) and not line.startswith("    "):




            insert_idx = i
            break

    lines.insert(insert_idx, f"from typing import {name}")
    return "\n".join(lines) + "\n"


def fix_builtins_any(content: str, line_num: int) -> str:
    lines = content.splitlines()
    if line_num > len(lines):










        return content
    line = lines[line_num - 1]
    # Only replace if used as a type hint (e.g. after : or ->)
    new_line = re.sub(r"([:->]\s*)\bany\b", r"\1Any", line)
    if new_line != line:
        lines[line_num - 1] = new_line



        return fix_missing_import("\n".join(lines) + "\n", 'Suggestion: "from typing import Any"')
    return content


def fix_implicit_optional(content: str, line_num: int, message: str) -> str:
    match = re.search(r'argument "([^"]+)" \(default has type "None", argument has type "([^"]+)"\)', message)
    if not match:
        return content
    arg_name, arg_type = match.groups()










    lines = content.splitlines()
    if line_num > len(lines):
        return content
    line = lines[line_num - 1]
    # pattern: arg_name: arg_type = None
    pattern = rf"({re.escape(arg_name)}\s*:\s*){re.escape(arg_type)}(\s*=\s*None)"
    new_line = re.sub(pattern, rf"\1{arg_type} | None\2", line)
    if new_line != line:
        lines[line_num - 1] = new_line
        return "\n".join(lines) + "\n"
    return content

def main():
    if not FIXES_DIR.exists():
        FIXES_DIR.mkdir(parents=True)

    file_issues = parse_mypy_log()










    files = sorted(list(file_issues.keys()))
    print(f"Found {len(files)} files with issues.")

    for file_rel in files:
        file_path = WS_ROOT / file_rel
        if not file_path.exists(): continue

        print(f"Processing {file_rel}...")
        safe_name = file_rel.replace("\\", "_").replace("/", "_")
        backup_diff_path = FIXES_DIR / f"{safe_name}.backup.diff"





        fix_diff_path = FIXES_DIR / f"{safe_name}.fix.diff"

        run_cmd(f"git diff HEAD {file_rel} > {backup_diff_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        # Apply line-by-line fixes in reverse
        issues = sorted(file_issues[file_rel], key=lambda x: x['line'], reverse=True)

        for issue in issues:
            msg = issue['message']
            line = issue['line']
            lines = new_content.splitlines()
            if line > len(lines): continue
            line_idx = line - 1
            l_content = lines[line_idx]

            if "builtins.any" in msg:
                new_content = fix_builtins_any(new_content, line)
            elif "Incompatible default for argument" in msg:
                new_content = fix_implicit_optional(new_content, line, msg)
            elif "Incompatible types in assignment" in msg and 'type "None"' in msg and 'type Module' in msg:
                if "type: ignore" not in l_content:
                    lines[line_idx] = l_content + "  # type: ignore[assignment]"
                    new_content = "\n".join(lines) + "\n"
            elif "Module has no attribute" in msg or "Module \"rust_core\" has no attribute" in msg:
                if "type: ignore" not in l_content:
                    lines[line_idx] = l_content + "  # type: ignore[attr-defined]"





                    new_content = "\n".join(lines) + "\n"
            elif "Need type annotation for" in msg:
                # E.g. Need type annotation for "hash_weights" (hint: "hash_weights: dict[<type>, <type>] = ...")
                match = re.search(r'hint: "([^"]+) = \.\.\."', msg)
                if match:
                    hint = match.group(1)  # "hash_weights: dict[<type>, <type>]"
                    # Try to replace name with hint
                    name = hint.split(":")[0].strip()
                    if f"{name} =" in l_content:
                        lines[line_idx] = l_content.replace(f"{name} =", f"{hint} =")
                        # Replace <type> with Any
                        lines[line_idx] = lines[line_idx].replace("<type>", "Any")
                        new_content = "\n".join(lines) + "\n"
                        new_content = fix_missing_import(new_content, 'Suggestion: "from typing import Any"')
            elif "Did you forget to import" in msg or ("Name" in msg and "is not defined" in msg):
                new_content = fix_missing_import(new_content, msg)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            run_cmd(f"git diff {file_rel} > {fix_diff_path}")
            print(f"  Fixed issues in {file_rel}")
            # Use current python to check syntax
            check_res = run_cmd(f"C:/DEV/PyAgent/.venv/Scripts/python.exe -m py_compile {file_rel}")
            if check_res.returncode != 0:
                print(f"  SYNTAX ERROR in {file_rel}! Reverting...")
                run_cmd(f"git checkout {file_rel}")
        else:
            print(f"  No automated fixes applied to {file_rel}")






if __name__ == "__main__":
    main()
