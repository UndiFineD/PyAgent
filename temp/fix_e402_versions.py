import os
import re




def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern:
    # from src.core.base.version import VERSION
    # __version__ = VERSION
    # with optional comments and empty lines between/around them

    # We want to find these and move them after all other top-level imports.

    version_import_re = re.compile(r"^from src\.core\.base\.version import VERSION\s*$", re.MULTILINE)
    version_assign_re = re.compile(r"^__version__ = VERSION\s*$", re.MULTILINE)

    has_import = version_import_re.search(content)
    has_assign = version_assign_re.search(content)

    if not (has_import and has_assign):
        return False

    # Remove them from their current positions
    new_content = version_import_re.sub("", content)
    new_content = version_assign_re.sub("", new_content)

    # Find the last top-level import
    lines = new_content.splitlines()
    last_import_idx = -1










    for i, line in enumerate(lines):
        if line.startswith(("import ", "from ")):
            last_import_idx = i




    if last_import_idx == -1:
        # No other imports? Just put it at the top then, but something is weird.
        return False

    # Insert them after the last import


    lines.insert(last_import_idx + 1, "from src.core.base.version import VERSION")
    lines.insert(last_import_idx + 2, "__version__ = VERSION")

    final_content = "\n".join(lines)





    if final_content != content:

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        return True
    return False




def main():
    count = 0
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                if fix_file(os.path.join(root, file)):
                    count += 1
    print(f"Fixed {count} files.")




if __name__ == "__main__":
    main()
