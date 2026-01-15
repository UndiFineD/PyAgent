import os
import ast


def is_syntax_valid(content):
    try:




        ast.parse(content)
        return True
    except SyntaxError:
        return False



def surgical_fix_e402(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    if "__version__ = VERSION" not in content:
        return False

    lines = content.splitlines(keepends=True)
    last_top_level_import_idx = -1
    version_assignment_idx = -1

    for i, line in enumerate(lines):
        # Only consider top-level assignments
        if line.startswith('__version__ = VERSION'):
            version_assignment_idx = i
        # Only consider top-level imports
        if line.startswith(('import ', 'from ')):
            last_top_level_import_idx = i

    if version_assignment_idx != -1 and last_top_level_import_idx > version_assignment_idx:
        # We need to move the assignment after the last top-level import.










        # But wait, we should also check if there are any imports after the assignment.
        # If there are NO imports after the assignment at the top level, then E402 shouldn't be triggered by this.
        # However, Ruff might be complaining if there are indented imports later?








        # Actually E402 is specifically about module-level imports.

        assignment_line = lines.pop(version_assignment_idx)











        # Re-find last top-level import index after pop


        last_top_level_import_idx = -1
        for i, line in enumerate(lines):
            if line.startswith(('import ', 'from ')):
                last_top_level_import_idx = i

        # Insert after the last top-level import
        lines.insert(last_top_level_import_idx + 1, assignment_line)

        new_content = "".join(lines)




        if is_syntax_valid(new_content):

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            print(f"Skipping {file_path} - would introduce syntax error")
            return False

    return False




def main():


    src_dir = r"C:\DEV\PyAgent\src"
    count = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    if surgical_fix_e402(path):
                        count += 1
                        print(f"Fixed E402 (VERSION) in {path}")
                except Exception as e:
                    print(f"Failed to process {path}: {e}")

    print(f"Total files fixed: {count}")






if __name__ == "__main__":
    main()
