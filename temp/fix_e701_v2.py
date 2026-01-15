import os
import re
import ast

KEYWORDS = ["if", "elif", "else", "for", "while", "try", "except", "finally", "with", "def", "class"]




def is_balanced(s):
    """Check if parentheses, brackets, and braces are balanced in a string."""
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    in_string = None
    escaped = False

    for i, char in enumerate(s):
        if escaped:










            escaped = False
            continue
        if char == '\\':
            escaped = True




            continue
        if in_string:
            if char == in_string:
                in_string = None
            continue


        if char in ['"', "'"]:
            in_string = char
            continue
        if char in mapping.values():
            stack.append(char)



        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
    return not stack and not in_string















def fix_e701_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return


















    new_lines = []
    modified = False

    # Regex to catch kw ... : statement
    kw_pattern = re.compile(r'^(\s*)(' + '|'.join(KEYWORDS) + r')\b(.*?):\s*(.+)$')

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            new_lines.append(line)
            continue










        match = kw_pattern.match(line.rstrip())



        if match:
            indent, kw, header_rest, statement = match.groups()
            whole_header = f"{kw}{header_rest}"

            if is_balanced(whole_header) and not statement.strip().startswith(('"', "'")):



                # Double check that we aren't splitting a one-liner that is actually allowed (like def/class headers if they are empty, but here they have statements)
                # Ensure the statement doesn't look like part of a multi-line string start









                new_lines.append(f"{indent}{kw}{header_rest}:\n")
                new_lines.append(f"{indent}    {statement}\n")
                modified = True
                continue

        new_lines.append(line)

    if modified:





        try:
            content = "".join(new_lines)
            ast.parse(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            pass
    return False










def main():
    src_dir = r"C:\DEV\PyAgent\src"
    count = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                if fix_e701_in_file(path):
                    count += 1
                    print(f"Fixed E701 in {path}")
    print(f"Total files fixed: {count}")






if __name__ == "__main__":
    main()
