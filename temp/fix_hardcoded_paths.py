import os
import re
from pathlib import Path




def fix_hardcoded_paths():
    root_dir = Path("C:/DEV/PyAgent")

    # regex for c:/DEV/PyAgent or C:/DEV/PyAgent or c:\\DEV\\PyAgent
    pattern = re.compile(r'c:/DEV/PyAgent', re.IGNORECASE)

    # Scan src and tests
    for target_dir in [root_dir / "src", root_dir / "tests"]:
        if not target_dir.exists(): continue
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    content = file_path.read_text(encoding="utf-8")

                    if pattern.search(content):
                        print(f"Fixing {file_path}")
                        # Determine parents count based on depth from root
                        rel_path = file_path.relative_to(root_dir)
                        parents_count = len(rel_path.parents) - 1

                        prefix = f"Path(__file__).resolve().parents[{parents_count}]"

                        # Replace full paths or partial paths starting with root
                        def replacer(match):
                            # We want to replace "C:/DEV/PyAgent/..." with Path(...) / "..."
                            # But wait, we need to handle quotes.
                            return "{ROOT_PLACEHOLDER}"

                        # Simpler: replace the string root with {ROOT} and then fix it up
                        content = content.replace("c:/DEV/PyAgent", "C:/DEV/PyAgent")
                        content = content.replace("C:/DEV/PyAgent", "{ROOT}")

                        # Fix up: "Path(__file__).resolve().parents[N] / 'src'"
                        # But wait, if it was in a string: "C:/DEV/PyAgent/src" -> "{ROOT}/src"










                        # We need to change the string to a Path object or similar.

                        # Search for "{ROOT}/..." inside strings
                        # e.g. "Path('{ROOT}/src')" or just "{ROOT}/src"





                        # Let's try something simpler:
                        # Replace '"C:/DEV/PyAgent' with 'str(Path(__file__).resolve().parents[N])' + '
                        content = content.replace('"{ROOT}', f'str({prefix}) + "')
                        content = content.replace("'{ROOT}", f"str({prefix}) + '")


                        # And handle cases where it's the exact string
                        content = content.replace(f'"{prefix}"', prefix)
                        content = content.replace(f"'{prefix}'", prefix)




                        # Handle leftover {ROOT} if any
                        content = content.replace("{ROOT}", f"str({prefix})")

                        file_path.write_text(content, encoding="utf-8")





if __name__ == "__main__":
    fix_hardcoded_paths()
