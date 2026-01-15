import os
import ast
import re




def scan_files(root_dir):
    results = {
        "bare_excepts": [],
        "print_statements": [],
        "large_files": [],
        "undocumented_classes": [],
        "todos": []
    }

    for root, dirs, files in os.walk(root_dir):
        if "node_modules" in root or ".venv" in root or "__pycache__" in root or "rust_core" in root:
            continue

        for file in files:
            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Large files
                if len(content) > 25000:
                    results["large_files"].append((rel_path, len(content)))

                # TODOs
                todo_matches = re.finditer(r"#\s*TODO:?\s*(.*)", content, re.IGNORECASE)
                for match in todo_matches:
                    results["todos"].append((rel_path, match.group(1).strip()))

                # Print statements
                print_matches = re.finditer(r"^\s*print\(", content, re.MULTILINE)
                for _ in print_matches:
                    results["print_statements"].append(rel_path)

                # AST analysis
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    # Bare excepts










                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        line_no = node.lineno
                        # Check if it was already fixed with a comment or pass
                        # (Basic heuristic: if content has 'except Exception' it's already caught by regex if I use string search,




                        # but AST is more precise for 'bare')
                        results["bare_excepts"].append((rel_path, line_no))

                    # Undocumented classes
                    if isinstance(node, ast.ClassDef):


                        docstring = ast.get_docstring(node)
                        if not docstring:
                            results["undocumented_classes"].append((rel_path, node.name, node.lineno))

            except Exception:



                # print(f"Error scanning {file_path}: {e}")
                pass

    return results





if __name__ == "__main__":
    src_dir = os.path.join(os.getcwd(), "src")
    report = scan_files(src_dir)

    print("--- SCAN REPORT ---")
    print(f"Bare Excepts: {len(report['bare_excepts'])}")
    for file, line in report["bare_excepts"][:10]:
        print(f"  {file}:{line}")

    print(f"\nLarge Files: {len(report['large_files'])}")
    for file, size in sorted(report["large_files"], key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {file} ({size} bytes)")

    print(f"\nUndocumented Classes: {len(report['undocumented_classes'])}")
    for file, name, line in report["undocumented_classes"][:10]:
        print(f"  {file}:{line} ({name})")

    print(f"\nTODOs: {len(report['todos'])}")
    for file, task in report["todos"][:10]:
        print(f"  {file}: {task}")

    # Write full results to a file for later processing
    import json
    with open("temp/scan_results.json", "w") as f:
        json.dump(report, f, indent=2)
