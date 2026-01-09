import os
import re

def fix_future_ordering(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if "from __future__" in content and "__logic_category__" in content:
                        lines = content.splitlines()
                        future_idx = -1
                        logic_idx = -1
                        for i, line in enumerate(lines):
                            if "from __future__" in line:
                                future_idx = i
                                break
                        for i, line in enumerate(lines):
                            if "__logic_category__" in line:
                                logic_idx = i
                                break
                        
                        if logic_idx != -1 and future_idx != -1 and logic_idx < future_idx:
                            print(f"Fixing {path}")
                            logic_line = lines.pop(logic_idx)
                            # Re-find future index after pop
                            for i, line in enumerate(lines):
                                if "from __future__" in line:
                                    future_idx = i
                                    break
                            
                            lines.insert(future_idx + 1, logic_line)
                            with open(path, "w", encoding="utf-8") as f:
                                f.write("\n".join(lines) + "\n")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    fix_future_ordering("src")
