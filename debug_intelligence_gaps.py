import os
import re

root = "src"
io_pattern = r"(requests\.(get|post|put|delete|patch|head)\(|self\.ai|subprocess\.(run|call|Popen|check_call|check_output)\(|adb shell|sqlite3\.(connect|execute|read_sql)|pd\.read_sql)"
findings = []

for r, d, files in os.walk(root):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(r, f)
            # print(f"Checking {path}")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    if re.search(io_pattern, content):
                        if not any(x in content for x in ["_record", "record_lesson", "record_interaction"]):
                             findings.append(path)
            except Exception:
                pass

print("\n".join(findings))
