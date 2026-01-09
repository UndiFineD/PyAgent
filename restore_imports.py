import os
import re

src_path = r"c:\DEV\PyAgent\src"
print(f"Starting import restoration in: {src_path}")

files_processed = 0
files_modified = 0

for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            files_processed += 1
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if "# Auto-removed unused" in content:
                    print(f"  Checking {file}...")
                    # Replace "# X # Auto-removed unused" with "X"
                    # Improved regex to be more flexible with leading hash and multiple suffixes
                    new_content = content
                    changes_in_file = 0
                    
                    # Pattern for lines that were commented out with the suffix
                    # Capture the leading indentation
                    pattern = r"^(\s*)#+\s*(.*?)\s*# Auto-removed unused.*$"
                    
                    lines = new_content.splitlines()
                    for i, line in enumerate(lines):
                        if "# Auto-removed unused" in line:
                            match = re.match(pattern, line)
                            if match:
                                indent = match.group(1)
                                restored = match.group(2)
                                # Repeatedly strip if multiple patterns remain
                                while "# Auto-removed unused" in restored:
                                    # Strip leading hash and trailing suffix again
                                    inner_match = re.match(r"^\s*#+\s*(.*?)\s*# Auto-removed unused.*$", restored)
                                    if inner_match:
                                        restored = inner_match.group(1)
                                    else:
                                        # If it has the suffix but not the leading hash, just strip suffix
                                        restored = re.sub(r"\s*# Auto-removed unused.*$", "", restored)
                                
                                print(f"    Restoring line {i+1}: {indent}{restored.strip()}")
                                lines[i] = f"{indent}{restored}"
                                changes_in_file += 1
                            else:
                                # If it doesn't have the leading hash but has the suffix
                                if "# Auto-removed unused" in line:
                                    restored = re.sub(r"\s*# Auto-removed unused.*$", "", line)
                                    print(f"    Restoring line {i+1} (suffix only): {restored.strip()}")
                                    lines[i] = restored
                                    changes_in_file += 1

                    if changes_in_file > 0:
                        new_content = "\n".join(lines) + ("\n" if content.endswith("\n") else "")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"  Modified: {path} ({changes_in_file} lines restored)")
                        files_modified += 1
            except Exception as e:
                print(f"  Error processing {path}: {e}")

print(f"\nFinished. Processed {files_processed} files, modified {files_modified} files.")
