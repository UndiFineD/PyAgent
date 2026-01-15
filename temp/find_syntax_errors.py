import ast
import os




def find_syntax_errors(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):


                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        ast.parse(f.read())
                except SyntaxError as e:


                    print(f"Syntax Error in {path}: {e}")
                except Exception:
                    # Some files might have encoding issues
                    pass


if __name__ == "__main__":
    find_syntax_errors('src')
