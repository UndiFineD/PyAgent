
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set

MYPY_LOG = r"mypy_after_v3.txt"
FIXES_DIR = Path(r"docs\work\mypy-fixes-v4")
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





def get_needed_imports(content: str, issues: List[dict]):
    typing_needed = set()
    pathlib_needed = False






    for issue in issues:
        msg = issue['message']
        # Check for undefined names
        match = re.search(r'Name "([^"]+)" is not defined', msg)
        if match:
            name = match.group(1)
            if name == "Path":
                pathlib_needed = True
            elif name in ["List", "Dict", "Any", "Optional", "Tuple", "Union", "Callable", "Set", "Type", "Iterable"]:
                typing_needed.add(name)

        # Check for type suggestions
        match = re.search(r'Suggestion: "from typing import ([^"]+)"', msg)
        if match:

            typing_needed.add(match.group(1))

    # Filter already present
    final_typing = set()
    for name in typing_needed:
        if not re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) and not re.search(rf"\bimport typing\b", content):
            final_typing.add(name)

    final_pathlib = False
    if pathlib_needed:
        if not re.search(r"\bfrom pathlib import\b.*?\bPath\b", content) and not re.search(r"\bimport pathlib\b", content):
            final_pathlib = True

    return final_typing, final_pathlib





def main():
    if not FIXES_DIR.exists():
        FIXES_DIR.mkdir(parents=True)

    file_issues = parse_mypy_log()
    files = sorted(list(file_issues.keys()))
    print(f"Found {len(files)} files with issues.")

    for file_rel in files:
        file_path = WS_ROOT / file_rel
        if not file_path.exists():
            # Try to see if it's a relative path starting from root elsewhere
            continue

        print(f"Processing {file_rel}...")
        safe_name = file_rel.replace("\\", "_").replace("/", "_")
        backup_diff_path = FIXES_DIR / f"{safe_name}.backup.diff"
        fix_diff_path = FIXES_DIR / f"{safe_name}.fix.diff"

        # Backup current state
        run_cmd(f"git diff {file_rel} > {backup_diff_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()

        # 1. Line-level fixes in reverse order to keep indices valid
        issues = sorted(file_issues[file_rel], key=lambda x: x['line'], reverse=True)

        for issue in issues:
            msg = issue['message']
            line_num = issue['line']
            if line_num > len(lines): continue










            idx = line_num - 1
            line = lines[idx]

            # already defined rc
            if "already defined (by an import)" in msg and " \"rc\" " in msg:
                if "# type: ignore" not in line:
                    lines[idx] = line + "  # type: ignore[no-redef]"

            # Module has no attribute (rust_core attributes)
            elif "Module has no attribute" in msg and idx > 0:

                if "rc." in line or "rust_core." in line:
                    if "# type: ignore" not in line:
                        lines[idx] = line + "  # type: ignore[attr-defined]"

            # any -> Any
            elif "builtins.any" in msg:
                # Replace 'any' with 'Any' if it looks like a type usage
                new_line = re.sub(r":\s*\bany\b", ": Any", line)
                new_line = re.sub(r"->\s*\bany\b", "-> Any", new_line)
                new_line = re.sub(r"\[\s*\bany\b", "[Any", new_line)
                new_line = re.sub(r"\bany\b\s*\]", "Any]", new_line)
                new_line = re.sub(r",\s*\bany\b", ", Any", new_line)
                lines[idx] = new_line






            # Incompatible types in assignment (None to Module)
            elif "Incompatible types in assignment" in msg and 'type "None"' in msg and 'type Module' in msg:
                if "# type: ignore" not in line:
                    lines[idx] = line + "  # type: ignore[assignment]"

        # 2. Add imports
        typing_needed, pathlib_needed = get_needed_imports("\n".join(lines), file_issues[file_rel])

        if typing_needed or pathlib_needed:
            # Find insertion point (after __future__ or at first import)
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("from __future__"):
                    insert_idx = i + 1
                elif line.strip().startswith("#") or line.strip() == "":
                    continue
                elif (line.startswith("import ") or line.startswith("from ")) and not line.startswith("    "):
                    insert_idx = i
                    break

            if pathlib_needed:
                lines.insert(insert_idx, "from pathlib import Path")

            if typing_needed:
                # Group them





                imp_list = sorted(list(typing_needed))
                lines.insert(insert_idx, f"from typing import {', '.join(imp_list)}")

        new_content = "\n".join(lines) + ("\n" if lines else "")

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            run_cmd(f"git diff {file_rel} > {fix_diff_path}")
            print(f"  Applied fixes to {file_rel}")

            # Verify syntax
            check_res = run_cmd(f"python -m py_compile {file_rel}")
            if check_res.returncode != 0:
                print(f"  !!! SYNTAX ERROR in {file_rel}, reverting...")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
        else:
            print(f"  No changes for {file_rel}")





if __name__ == "__main__":
    main()
