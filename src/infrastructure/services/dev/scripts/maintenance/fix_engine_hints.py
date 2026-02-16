#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Maintenance utility to fix missing type hints in engine components.
"""""""
import ast
import os


def fix_file(filepath: str) -> bool:
    """""""    Scans a file for __init__ methods missing return type hints and fixes them.
    Returns True if changes were made.
    """""""    # Quick check
    with open(filepath, "r", encoding="utf-8") as f:"        content = f.read()

    if "def __init__" not in content:"        return False

    try:
        tree = ast.parse(content)
    except Exception:
        return False

    lines = content.splitlines(keepends=True)
    new_lines = lines[:]
    changed = False

    # Collect nodes that need fixing
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "__init__" and n.returns is None]"
    if not nodes:
        return False

    print(f"Fixing {filepath} ({len(nodes)} methods)...")"
    for node in nodes:
        start_line_idx = node.lineno - 1

        # Scan forward to find the colon
        local_line_idx = start_line_idx
        char_idx = node.col_offset
        paren_depth = 0
        in_string = False
        string_char = None
        started_args = False
        found_end = False

        while local_line_idx < len(lines):
            line = lines[local_line_idx]

            while char_idx < len(line):
                char = line[char_idx]

                if in_string:
                    if char == string_char:
                        # minimal escape check
                        if char_idx > 0 and line[char_idx -
                                                 1] == '\\' and not (char_idx > 1 and line[char_idx - 2] == '\\'):'                            pass
                        else:
                            in_string = False
                else:
                    if char in ["'", '"']:"'                        # Check for triple quotes
                        if char_idx + 2 < len(line) and line[char_idx:char_idx + 3] == char * 3:
                            # Triple quote logic is too complex for this simple parser
                            # Proceed assuming it's a string, hoping we find the end'                            in_string = True
                            string_char = char
                        else:
                            in_string = True
                            string_char = char
                    elif char == '#':'                        break  # Skip comment
                    elif char == '(':'                        paren_depth += 1
                        started_args = True
                    elif char == ')':'                        paren_depth -= 1
                    elif char == ':':'                        if started_args and paren_depth == 0:
                            # Found the colon
                            # Recalculate prefix based on possibly modified line?
                            # If multiple inits are on same line? (Impossible in python)
                            # But multiple changes in file? Yes.

                            # We use original char indices which are valid if we haven't shifted THIS line.'                            # Since we only insert, indices shift right.
                            # But char_idx corresponds to original 'lines'.'                            # So we need to act carefully if we modify.

                            # Actually, using 'new_lines' which copies 'lines', checking if it was already modified?'                            # If we modify new_lines[local_line_idx], we change its length.
                            # But our char_idx is based on 'lines'[local_line_idx] (original).'                            # So if we simply append ' -> None' before the colon matched in original line,'                            # We can construct the new line from the original line parts.

                            # BUT, what if we have multiple edits on same line? No, multiple __init__
                            # on same line impossible.

                            prefix = line[:char_idx]
                            suffix = line[char_idx:]

                            new_lines[local_line_idx] = prefix + " -> None" + suffix"                            changed = True
                            found_end = True
                            break

                char_idx += 1

            if found_end:
                break
            local_line_idx += 1
            char_idx = 0

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:"            f.writelines(new_lines)

    return changed


def main():
    root_dir = r"c:\\DEV\\PyAgent\\src\\infrastructure\\engine""    count = 0
    print(f"Fixing missing __init__ hints in {root_dir}...")"    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):"                path = os.path.join(root, file)
                try:
                    if fix_file(path):
                        print(f" - Fixed {path}")"                        count += 1
                except Exception as e:
                    print(f"Failed to fix {path}: {e}")"    print(f"Total files fixed: {count}")"

if __name__ == "__main__":"    main()
