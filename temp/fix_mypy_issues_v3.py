
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set

MYPY_LOG = r"docs\work\mypy_final.txt"
FIXES_DIR = Path(r"docs\work\mypy-fixes-v3")
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



def get_required_imports(content: str, issues: List[dict]) -> Set[str]:
    needed = set()
    for issue in issues:
        msg = issue['message']
        match = re.search(r'Suggestion: "from typing import ([^"]+)"', msg)
        if match:

            needed.add(match.group(1))
        else:
            match = re.search(r'Name "([^"]+)" is not defined', msg)
            if match and match.group(1) in ["List", "Dict", "Any", "Optional", "Tuple", "Union", "Callable", "Set", "Type", "Iterable"]:
                needed.add(match.group(1))
        if "builtins.any" in msg:
            needed.add("Any")

    # Filter already present
    final_needed = set()
    for name in needed:
        if not re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) and not re.search(rf"\bimport typing\b", content):
            final_needed.add(name)
    return final_needed





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

        lines = content.splitlines()

        # 1. Line-level fixes in reverse
        issues = sorted(file_issues[file_rel], key=lambda x: x['line'], reverse=True)

        for issue in issues:
            msg = issue['message']





            line_num = issue['line']
            if line_num > len(lines): continue
            idx = line_num - 1
            line = lines[idx]

            if "builtins.any" in msg:
                # Replace 'any' with 'Any' if it looks like a type
                new_line = re.sub(r"\bany\b", "Any", line)
                lines[idx] = new_line
            elif "Incompatible default for argument" in msg:
                match = re.search(r'argument "([^"]+)" \(default has type "None", argument has type "([^"]+)"\)', msg)
                if match:
                    arg_name, arg_type = match.groups()



                    pattern = rf"({re.escape(arg_name)}\s*:\s*){re.escape(arg_type)}(\s*=\s*None)"
                    lines[idx] = re.sub(pattern, rf"\1{arg_type} | None\2", line)
            elif "Incompatible types in assignment" in msg and 'type "None"' in msg and 'type Module' in msg:
                if "type: ignore" not in line:
                    lines[idx] = line + "  # type: ignore[assignment]"



            elif "Module has no attribute" in msg or "Module \"rust_core\" has no attribute" in msg:
                if "type: ignore" not in line:
                    lines[idx] = line + "  # type: ignore[attr-defined]"
            elif "Need type annotation for" in msg:
                match = re.search(r'hint: "([^"]+) = \.\.\."', msg)
                if match:
                    hint = match.group(1).replace("<type>", "Any")
                    name = hint.split(":")[0].strip()
                    if f"{name} =" in line:
                        lines[idx] = line.replace(f"{name} =", f"{hint} =")

        # 2. Add imports
        needed_imports = get_required_imports("\n".join(lines), file_issues[file_rel])
        if needed_imports:
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("from __future__"):
                    insert_idx = i + 1
                elif line.strip().startswith("#") or line.strip() == "":
                    continue

                elif (line.startswith("import ") or line.startswith("from ")) and not line.startswith("    "):
                    insert_idx = i
                    break
            for imp in sorted(list(needed_imports)):
                lines.insert(insert_idx, f"from typing import {imp}")

        new_content = "\n".join(lines) + ("\n" if lines else "")

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            run_cmd(f"git diff {file_rel} > {fix_diff_path}")
            print(f"  Fixed issues in {file_rel}")
            check_res = run_cmd(f"C:/DEV/PyAgent/.venv/Scripts/python.exe -m py_compile {file_rel}")
            if check_res.returncode != 0:
                print(f"  SYNTAX ERROR in {file_rel}! Reverting...")
                run_cmd(f"git checkout {file_rel}")
        else:
            print(f"  No automated fixes applied to {file_rel}")






if __name__ == "__main__":
    main()
