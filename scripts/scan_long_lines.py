import os

def find_long_lines(root_dir, max_len=120):
    ignore_dirs = {'.venv', '.git', '__pycache__', 'node_modules', 'dist', 'build', 'rust_core', 'data'}
    results = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            clean_line = line.rstrip('\r\n')
                            if len(clean_line) > max_len:
                                results.append(f"{path}:{i}:{len(clean_line)}")
                except Exception as e:
                    print(f"Error reading {path}: {e}")
    return results

if __name__ == "__main__":
    long_lines = find_long_lines('.')
    with open('long_lines_report.txt', 'w', encoding='utf-8') as f:
        for line in long_lines:
            f.write(line + '\n')
    print(f"Found {len(long_lines)} lines longer than 120 chars. Report saved to long_lines_report.txt")
