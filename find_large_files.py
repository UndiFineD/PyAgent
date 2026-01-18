import os

src_dir = r"c:\DEV\PyAgent\src"
large_files = []

for root, dirs, files in os.walk(src_dir):
    if "__pycache__" in root:
        continue
    
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.count("\n") + 1
                
                # Check if it's a facade - usually in the first few hundred chars
                first_part = content[:500].lower()
                is_facade = "facade" in first_part
                
                if lines > 500 and not is_facade:
                    large_files.append((path, lines))

large_files.sort(key=lambda x: x[1], reverse=True)

print(f"{'Path':<80} {'LineCount':<10}")
print("-" * 90)
for p, c in large_files[:5]:
    print(f"{p:<80} {c:<10}")
