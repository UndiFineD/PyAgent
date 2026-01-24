import os
import re

files_to_fix = [
    "tests/integration/test_backend_integration.py",
    "tests/integration/test_coder_logic_integration.py",
    "tests/integration/test_context_integration.py",
    "tests/unit/logic/advanced.py",
    "tests/unit/observability/advanced.py",
    "tests/unit/observability/edge_cases.py",
    "tests/unit/observability/test_reports_integration.py",
    "tests/unit/observability/test_reports_performance.py",
    "tests/unit/observability/test_stats_performance.py",
]

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Add Self to typing import
    if "from typing import" in content:
        # Check if already has Self
        if "Self" not in content.split("\n")[0:20]: # rough check
            content = re.sub(r"from typing import ([^\n]+)", r"from typing import \1, Self", content, count=1)
            # Cleanup if Multi-line or already has some
            content = content.replace(", ,", ",")
            content = content.replace(", Self, Self", ", Self")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed {filepath}")

if __name__ == "__main__":
    for f in files_to_fix:
        fix_file(f)
