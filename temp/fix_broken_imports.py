
import os
from pathlib import Path

WS_ROOT = Path(r"c:\DEV\PyAgent")

CORE_TYPES = [
    "ChangelogEntry", "ReleaseNote", "ComplianceCategory", "ComplianceResult",
    "MonorepoEntry", "SearchResult", "LocalizationLanguage", "LocalizedEntry",
    "DiffResult", "DiffViewMode", "FeedFormat", "LinkedReference", "VersioningStrategy", "TemplateManager"
]

def fix_imports():



    for root, dirs, files in os.walk(WS_ROOT / "src"):
        # Skip core/base/types itself if we want, but actually relative imports there ARE correct.
        # But wait, if they are in the same folder, .ClassName is fine.
        # The problem is when they are NOT in the same folder.

        rel_dir = os.path.relpath(root, WS_ROOT)
        is_types_dir = "src\\core\\base\\types" in rel_dir or "src/core/base/types" in rel_dir

        for file in files:
            if not file.endswith(".py"): continue
            file_path = Path(root) / file

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content
            for cls in CORE_TYPES:
                # Find "from .ClassName import ClassName"
                pattern = rf"from \.{cls} import {cls}"

                # If we are NOT in the types dir, this is likely wrong if the file isn't there.



                if not is_types_dir:



                    if pattern in new_content:



                        # Check if ClassName.py exists in THIS directory
                        if not (Path(root) / f"{cls}.py").exists():
                            print(f"Fixing {cls} import in {file_path}")
                            new_content = new_content.replace(pattern, f"from src.core.base.types import {cls}")


            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

if __name__ == "__main__":




    fix_imports()
