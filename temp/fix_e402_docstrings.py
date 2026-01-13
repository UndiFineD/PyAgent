
import ast
import os
import sys

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False

    # Check for docstring (first expression that is a string)
    docstring_node = None
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, (ast.Str, ast.Constant)):
        val = tree.body[0].value
        if isinstance(val, ast.Str) or (isinstance(val, ast.Constant) and isinstance(val.value, str)):
            # It's already at the top
            docstring_node = tree.body[0]
    
    # Look for a string literal that is NOT at the top
    misplaced_docstring = None
    first_future = None
    first_import = None
    
    for i, node in enumerate(tree.body):
        if isinstance(node, ast.ImportFrom) and node.module == '__future__':
            if first_future is None:
                first_future = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if first_import is None:
                first_import = node
        elif isinstance(node, ast.Expr) and isinstance(node.value, (ast.Str, ast.Constant)):
            val = node.value
            if isinstance(val, ast.Str) or (isinstance(val, ast.Constant) and isinstance(val.value, str)):
                if i > 0: # Note: if i=0 it's already at top
                    misplaced_docstring = node
                    break
    
    if misplaced_docstring:
        # Check if it's misplaced relative to future or imports
        limit = None
        if first_future:
            limit = first_future.lineno
        elif first_import:
            limit = first_import.lineno
            
        if limit and misplaced_docstring.lineno > limit:
            # We found a misplaced docstring!
            lines = content.splitlines(keepends=True)
            
            # Extract docstring lines
            # Note: ast lineno is 1-based
            ds_start = misplaced_docstring.lineno - 1
            ds_end = misplaced_docstring.end_lineno
            ds_lines = lines[ds_start:ds_end]
            
            # Remove from original position
            new_lines = lines[:ds_start] + lines[ds_end:]
            
            # Find insertion point (before first_future or first_import)
            # We need to find where the line was in the new_lines
            # or just use the original limit and adjust
            insert_pos = 0
            # Skip shebang and comments at the top
            while insert_pos < len(new_lines):
                line = new_lines[insert_pos].strip()
                if not line or line.startswith('#') or line.startswith('from __future__'):
                    # We want it BEFORE __future__, so stop if we see it
                    if line.startswith('from __future__'):
                        break
                    insert_pos += 1
                else:
                    break
            
            final_lines = new_lines[:insert_pos] + ds_lines + ['\n'] + new_lines[insert_pos:]
            
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(final_lines)
            return True
            
    return False

def main():
    fixed_count = 0
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                if fix_file(path):
                    print(f"Fixed {path}")
                    fixed_count += 1
    print(f"Total fixed: {fixed_count}")

if __name__ == '__main__':
    main()
