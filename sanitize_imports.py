import os

src_path = r"c:\DEV\PyAgent\src"

def sanitize_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is an import starting at col 0
        stripped = line.lstrip()
        if (stripped.startswith("import ") or stripped.startswith("from ")) and line.startswith(stripped) and i > 0 and i < len(lines) - 1:
            # Look at previous line and next line
            prev_line = lines[i-1]
            next_line = lines[i+1]
            
            prev_indent = len(prev_line) - len(prev_line.lstrip())
            next_indent = len(next_line) - len(next_line.lstrip())
            
            if prev_indent > 0 and next_indent >= prev_indent:
                # This import is likely wrongly indented to col 0
                new_line = (" " * prev_indent) + line
                new_lines.append(new_line)
                print(f"  Fixed indentation in {path} line {i+1}")
                modified = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1
            
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    return modified

files_processed = 0
files_fixed = 0

for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            files_processed += 1
            if sanitize_file(os.path.join(root, file)):
                files_fixed += 1

print(f"Finished. Processed {files_processed} files, fixed {files_fixed} files.")
