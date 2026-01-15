import os
import ast




def check_node(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        # Remove docstrings from body for checking
        body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
        if not body: return True
        if len(body) > 1: return False
        stmt = body[0]
        if isinstance(stmt, ast.Pass): return True
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis: return True
        if isinstance(stmt, ast.Raise):
            exc_name = ""
            if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name): exc_name = stmt.exc.func.id
            elif isinstance(stmt.exc, ast.Name): exc_name = stmt.exc.id
            if exc_name == "NotImplementedError": return True
        return False
    if isinstance(node, ast.ClassDef):
        # Check if it's an ABC or Protocol - if so, it's not a "stub needing implementation" in the sense the user means










        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in ('ABC', 'Protocol'): return "IS_ABC"
            if isinstance(base, ast.Attribute) and base.attr in ('ABC', 'Protocol'): return "IS_ABC"






        # Check all members
        body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
        if not body: return True
        if len(body) == 1 and isinstance(body[0], ast.Pass): return True






        for item in body:

            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                res = check_node(item)
                if res is False: return False
                if res == "IS_ABC": return "IS_ABC"





            elif isinstance(item, ast.Pass): continue
            else: return False
        return True
    return True




def is_stub_file(path):
    if os.path.basename(path) == "__init__.py": return False
    try:
        with open(path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            has_definition = False
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    has_definition = True
                    res = check_node(node)




                    if res is False or res == "IS_ABC": return False
                elif isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
                    continue
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    continue
                else:
                    return False
            return has_definition
    except: return False






src_path = "c:/DEV/PyAgent/src"
stubs = []
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            if is_stub_file(full_path):
                stubs.append(full_path)

for stub in stubs:
    print(stub)
