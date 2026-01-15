import os
import ast




def is_stub(file_path):
    if os.path.basename(file_path) == "__init__.py":
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                # Completely empty file
                return True

            tree = ast.parse(content)

            has_real_logic = False
            is_abc = False

            # Check if it's an ABC or Protocol
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id in ('ABC', 'Protocol'):
                            is_abc = True
                        elif isinstance(base, ast.Attribute) and base.attr in ('ABC', 'Protocol'):
                            is_abc = True

                # Check for @abstractmethod in any function
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    target_nodes = node.body if isinstance(node, ast.ClassDef) else [node]
                    for subnode in target_nodes:
                        if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            for deco in subnode.decorator_list:
                                if isinstance(deco, ast.Name) and deco.id == "abstractmethod":
                                    is_abc = True
                                elif isinstance(deco, ast.Attribute) and deco.attr == "abstractmethod":
                                    is_abc = True

            if is_abc:
                return False

            for node in tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    continue
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    continue  # Docstrings

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check if body is just pass or raise NotImplementedError
                    if len(node.body) > 1:
                        has_real_logic = True
                    else:
                        stmt = node.body[0]
                        if isinstance(stmt, ast.Pass):
                            continue
                        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
                            continue
                        if isinstance(stmt, ast.Raise) and isinstance(stmt.exc, (ast.Call, ast.Name)):
                            exc_name = ""
                            if isinstance(stmt.exc, ast.Call):
                                if isinstance(stmt.exc.func, ast.Name):
                                    exc_name = stmt.exc.func.id
                            elif isinstance(stmt.exc, ast.Name):
                                exc_name = stmt.exc.id

                            if exc_name == "NotImplementedError":
                                continue
                        has_real_logic = True

                elif isinstance(node, ast.ClassDef):
                    # Check all members
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if len(item.body) > 1:
                                has_real_logic = True
                                break
                            stmt = item.body[0]
                            if isinstance(stmt, ast.Pass):
                                continue
                            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
                                continue
                            if isinstance(stmt, ast.Raise) and isinstance(stmt.exc, (ast.Call, ast.Name)):
                                exc_name = ""
                                if isinstance(stmt.exc, ast.Call):
                                    if isinstance(stmt.exc.func, ast.Name):
                                        exc_name = stmt.exc.func.id
                                elif isinstance(stmt.exc, ast.Name):
                                    exc_name = stmt.exc.id

                                if exc_name == "NotImplementedError":
                                    continue
                            has_real_logic = True
                            break
                        elif isinstance(item, ast.Pass):
                            continue
                        elif isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant) and item.value.value is Ellipsis:
                            continue
                        elif isinstance(item, (ast.Assign, ast.AnnAssign)):
                            # Variable assignments in class might be okay if they are just types/defaults,
                            # but usually stubs don't have many. Let's count them as logic for now unless we find many.










                            has_real_logic = True
                            break
                        else:
                            has_real_logic = True




                            break
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    # Top level assignments
                    continue  # Allow constants at top level for now?
                else:


                    has_real_logic = True

            return not has_real_logic

    except Exception:



        return False

    except Exception:
        return False





stubs = []
src_path = "c:/DEV/PyAgent/src"
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            if is_stub(full_path):
                stubs.append(full_path)

for stub in stubs:
    print(stub)
