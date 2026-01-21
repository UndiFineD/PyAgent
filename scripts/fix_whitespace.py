"""Module to fix trailing whitespace in Python files."""
import os

def fix_whitespace_in_file(file_path):
    """Removes trailing whitespace from each line in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    for line in lines:
        # Remove trailing whitespace but keep newline
        stripped = line.rstrip()
        if stripped != line.rstrip('\n'):
            changed = True
        new_lines.append(stripped + '\n')

    if changed:
        print(f"Fixing whitespace in {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    """Main entry point to walk through python files and fix whitespace."""
    exclude_dirs = {'.venv', 'node_modules', '.git', '__pycache__', 'target'}
    for root, dirs, _ in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in os.listdir(root):
            if name.endswith('.py'):
                fix_whitespace_in_file(os.path.join(root, name))

if __name__ == "__main__":
    main()
