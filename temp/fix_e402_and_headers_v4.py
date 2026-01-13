import ast
import os
import sys

def fix_imports_and_headers(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return

    try:
        tree = ast.parse(content)
    except Exception as e:
        # Skip files with syntax errors
        return

    lines = content.splitlines()
    
    # 1. Identify all top-level import nodes
    import_nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    if not import_nodes:
        return

    # 2. Get line indices for imports
    import_line_indices = set()
    for node in import_nodes:
        # ast lineno is 1-indexed
        for i in range(node.lineno - 1, node.end_lineno):
            import_line_indices.add(i)

    # 3. Extract imports and non-imports
    extracted_imports = []
    for i in sorted(list(import_line_indices)):
        extracted_imports.append(lines[i])

    other_lines = [lines[i] for i in range(len(lines)) if i not in import_line_indices]

    # 4. Identify docstring position
    docstring_end_idx = -1
    # Check if first node is a docstring Expr
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, (ast.Constant, ast.Str)):
        # It's a docstring
        docstring_end_idx = tree.body[0].end_lineno - 1 # 0-indexed index in original lines

    # 5. Reconstruct file
    final_output = []
    
    # a. Shebang
    if other_lines and other_lines[0].startswith('#!'):
        final_output.append(other_lines.pop(0))

    # b. Header comments (License)
    # We'll take everything up to the first non-comment, non-empty line
    # but we'll stop if we hit something that looks like the END of the first block
    first_block_comments = []
    while other_lines and (other_lines[0].strip().startswith('#') or not other_lines[0].strip()):
        line = other_lines.pop(0)
        if line.strip() == "": continue # Skip empty lines in header for now
        first_block_comments.append(line)
    
    # Deduplicate lines in first_block_comments? Maybe later.
    final_output.extend(first_block_comments)
    final_output.append("") # One newline after license

    # c. Docstring
    # If there was a docstring, we need to extract it from 'other_lines'
    # Wait, the docstring might have been at index docstring_end_idx in 'lines'
    # but now 'other_lines' is different.
    # Let's just find the first line in 'other_lines' that starts with triple quotes.
    if other_lines and (other_lines[0].strip().startswith('"""') or other_lines[0].strip().startswith("'''")):
        while other_lines:
            l = other_lines.pop(0)
            final_output.append(l)
            if '"""' in l or "'''" in l:
                if l.count('"""') == 2 or l.count("'''") == 2:
                    break
                # Multi-line
                while other_lines:
                    l2 = other_lines.pop(0)
                    final_output.append(l2)
                    if '"""' in l2 or "'''" in l2:
                        break
                break
        final_output.append("")

    # d. Future imports
    future_imports = [i for i in extracted_imports if '__future__' in i]
    other_imports = [i for i in extracted_imports if '__future__' not in i]
    
    final_output.extend(future_imports)
    final_output.extend(other_imports)
    final_output.append("")

    # e. The rest of the file (and we'll strip out repeated license lines)
    license_markers = [
        "Copyright 2026 PyAgent Authors",
        "Licensed under the Apache License",
        "you may not use this file except in compliance",
        "http://www.apache.org/licenses/LICENSE-2.0"
    ]
    
    for line in other_lines:
        # Crude deduplication: if it's a comment and contains a license marker, skip it
        # UNLESS we are in the first 50 lines (but we already popped the first block)
        is_license = any(marker in line for marker in license_markers)
        if is_license:
            continue
        final_output.append(line)

    # Final cleanup: ensure no massive empty blocks
    new_content = "\n".join(final_output)
    # Replace 3+ newlines with 2
    import re
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    # Validation
    try:
        ast.parse(new_content)
    except Exception as e:
        print(f"Skipping {path} - resulting code is invalid: {e}")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {path}")

def main():
    target_dir = 'src'
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                fix_imports_and_headers(path)

if __name__ == "__main__":
    main()
