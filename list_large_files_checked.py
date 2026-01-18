import os

root = r"c:\DEV\PyAgent\src"
results = []

for dirpath, dirnames, filenames in os.walk(root):
    if "__pycache__" in dirpath:
        continue
    for filename in filenames:
        if filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            try:
                # Use binary or careful encoding to count lines accurately
                with open(filepath, 'rb') as f:
                    content = f.read()
                    line_count = content.count(b'\n') + (1 if content and not content.endswith(b'\n') else 0)
                
                if line_count > 600:
                    size = len(content)
                    # Check if it's a facade (very low byte count per line)
                    # or just small absolute size.
                    # The user mentioned "they don't have thousands of bytes of code".
                    # Most 600 line files will have 10-20KB.
                    # If a file has 600 lines but only 2000 bytes, that's ~3 bytes per line. That's a facade.
                    is_facade = size < 5000 # Heuristic for "thousands of bytes"
                    
                    rel_path = os.path.relpath(filepath, r"c:\DEV\PyAgent").replace("\\", "/")
                    results.append((line_count, rel_path, size, is_facade))
            except Exception as e:
                pass

results.sort(key=lambda x: x[0], reverse=True)
for count, path, size, is_facade in results:
    msg = f"{count} {path}"
    if is_facade:
        msg += f" (Note: Potentially a facade, size: {size} bytes)"
    print(msg)
