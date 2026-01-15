
import os
from pathlib import Path

WS_ROOT = Path(r"c:\DEV\PyAgent")

CORE_TYPES = [
    "ChangelogEntry", "ReleaseNote", "ComplianceCategory", "ComplianceResult",
    "MonorepoEntry", "SearchResult", "LocalizationLanguage", "LocalizedEntry",
    "DiffResult", "DiffViewMode", "FeedFormat", "LinkedReference", "VersioningStrategy", "TemplateManager"
]

def fix_imports():



    print(f"Starting import fixes in {WS_ROOT / 'src'}...")
    count = 0
    for root, dirs, files in os.walk(WS_ROOT / "src"):
        rel_dir = os.path.relpath(root, WS_ROOT)
        is_types_dir = "core\\base\\types" in rel_dir or "core/base/types" in rel_dir

        for file in files:
            if not file.endswith(".py"): continue
            file_path = Path(root) / file

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            new_content = content
            for cls in CORE_TYPES:
                pattern = f"from .{cls} import {cls}"
                if pattern in new_content:
                    if not is_types_dir:
                        # Only fix if the file doesn't exist locally



                        local_file = Path(root) / f"{cls}.py"



                        if not local_file.exists():


                            print(f"  Fixing {cls} in {os.path.relpath(file_path, WS_ROOT)}")
                            new_content = new_content.replace(pattern, f"from src.core.base.types import {cls}")
                            count += 1

            if new_content != content:

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
    print(f"Done. Fixed {count} imports.")

if __name__ == "__main__":




    fix_imports()
