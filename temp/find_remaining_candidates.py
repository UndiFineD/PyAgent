import os
import subprocess
import re

def count_loops(file_path):
    try:
        # Use ripgrep to count for/while keywords
        result = subprocess.run(
            ['rg', '-c', 'for |while ', file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
        return 0
    except Exception:
        return 0

def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def find_candidates(root_dir):
    candidates = []
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.venv' in dirs:
            dirs.remove('.venv')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
            
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                loc = count_lines(path)
                if loc > 200:
                    loops = count_loops(path)
                    if loops > 3:
                        candidates.append((path, loc, loops))
    
    return sorted(candidates, key=lambda x: x[2], reverse=True)

if __name__ == "__main__":
    src_dir = os.path.join(os.getcwd(), 'src')
    candidates = find_candidates(src_dir)
    print(f"Found {len(candidates)} profiling candidates:")
    for path, loc, loops in candidates:
        print(f"{path}: LOC={loc}, Loops={loops}")
