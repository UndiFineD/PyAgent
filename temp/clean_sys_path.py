import os
import re
from pathlib import Path




def remove_sys_path_hacks():
    root_dir = Path("C:/DEV/PyAgent")
    tests_dir = root_dir / "tests"

    # Patterns to match:
    # sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))
    # sys.path.insert(0, str(AGENT_DIR))
    # etc.

    # We want to keep imports, but remove the sys.path manipulation.






    patterns = [
        re.compile(r'^\s*sys\.path\.insert\(.*?\)\s*$', re.MULTILINE),
        re.compile(r'^\s*sys\.path\.append\(.*?\)\s*$', re.MULTILINE)
    ]




    for root, dirs, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file


                content = file_path.read_text(encoding="utf-8")

                original_content = content
                for p in patterns:
                    content = p.sub('', content)




                if content != original_content:
                    print(f"Cleaning {file_path}")
                    file_path.write_text(content, encoding="utf-8")





if __name__ == "__main__":
    remove_sys_path_hacks()
