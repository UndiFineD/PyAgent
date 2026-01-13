import os
import re

def fix_e402_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    new_lines = []
    import_lines = []
    other_lines = []
    
    # We want to find all import statements and move them to the top, 
    # but after docstrings and __future__ imports.
    
    # First, separate docstrings and __future__ imports.
    header = []
    footer = []
    middle = []
    
    found_first_import = False
    
    # Simplified approach:
    # 1. Identify all module-level imports.
    # 2. Identify all module-level non-import statements.
    # 3. Reconstruct: docstring -> future imports -> all other imports -> everything else.
    
    docstring_end = -1
    # Check for triple quotes at the very beginning (ignoring shebang/comments)
    in_docstring = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not found_first_import and (stripped.startswith('"""') or stripped.startswith("'''")):
            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                docstring_end = i
                break
            in_docstring = True
            continue
        if in_docstring:
            if '"""' in line or "'''" in line:
                docstring_end = i
                in_docstring = False
                break
            continue
        if stripped and not stripped.startswith('#') and not stripped.startswith('!'):
            break

    # Now collect imports and others
    imports = []
    others = []
    
    current_import = []
    for i, line in enumerate(lines):
        if i <= docstring_end:
            header.append(line)
            continue
            
        stripped = line.strip()
        # Handle shebang and initial comments as header if not already in header
        if not header and (stripped.startswith('#') or stripped.startswith('!')):
            header.append(line)
            continue

        # Check if it's an import
        # This is a bit naive for multi-line imports without parens, but most our stuff uses parens or single line.
        if stripped.startswith('import ') or stripped.startswith('from '):
            imports.append(line)
            continue
            
        # If it's empty or a comment, keep it near where it was? 
        # Actually, let's just keep them in 'others' for now.
        if stripped:
            others.append(line)
        else:
            others.append(line)

    # This is too destructive. Let's try a more surgical approach for the VERSION issue.
    # Often it's:
    # import ...
    # __version__ = VERSION
    # <lots of comments/whitespace>
    # import ...
    
    return False

def surgical_fix_e402(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Target: __version__ = VERSION (or similar) followed by more imports
    # We want to move these assignments after the imports.
    
    modified = False
    
    # Pattern: a VERSION import and assignment
    pattern = re.compile(r'(from\s+[\w\.]+\s+import\s+VERSION\s*\n__version__\s*=\s*VERSION\s*\n)', re.MULTILINE)
    
    match = pattern.search(content)
    if match:
        version_block = match.group(1)
        # Find if there are more imports after this block
        rest = content[match.end():]
        if 'import ' in rest or 'from ' in rest:
            # Move the version block (specifically the assignment) down or move imports up.
            # Easiest: find the last import in the file and move the assignment after it.
            
            lines = content.splitlines(keepends=True)
            last_import_idx = -1
            version_assignment_idx = -1
            
            for i, line in enumerate(lines):
                if '__version__ = VERSION' in line:
                    version_assignment_idx = i
                if line.strip().startswith(('import ', 'from ')):
                    last_import_idx = i
            
            if last_import_idx > version_assignment_idx:
                # Move assignment to last_import_idx + 1
                assignment_line = lines.pop(version_assignment_idx)
                # Recalculate last_import_idx because we popped a line
                last_import_idx = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith(('import ', 'from ')):
                        last_import_idx = i
                
                lines.insert(last_import_idx + 1, assignment_line)
                new_content = "".join(lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True

    return False

def main():
    src_dir = r"C:\DEV\PyAgent\src"
    count = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                if surgical_fix_e402(path):
                    count += 1
                    print(f"Fixed E402 (VERSION) in {path}")
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    main()
