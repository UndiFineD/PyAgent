import os
import ast

def count_real_code(file_path):
    if os.path.basename(file_path) == "__init__.py":
        return 1000 # Ignore in this filter
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return 0
            
            tree = ast.parse(content)
            
            real_stmts = 0
            for node in tree.body: # Only top level
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    continue
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    continue # Docstrings
                
                real_stmts += 1
            
            return real_stmts
    except:
        return 1000

src_path = "c:/DEV/PyAgent/src"
stubs = []
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            count = count_real_code(path)
            if count <= 2: # Very few real statements
                stubs.append((path, count))

for path, count in sorted(stubs, key=lambda x: x[1]):
    print(f"{count}: {path}")
