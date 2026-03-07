#!/usr/bin/env python3

"""Lift non-typing imports from TYPE_CHECKING blocks to top-level."""

import pathlib


def process_file(path: pathlib.Path) -> bool:
    """Process a single file, lifting non-typing imports out of TYPE_CHECKING blocks."""
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        # skip non-text or problematic files
        return False
    if 'if TYPE_CHECKING' not in text:
        return False
    lines = text.splitlines()
    new_lines = []
    in_block = False
    to_lift = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('if TYPE_CHECKING'):
            new_lines.append(line)
            in_block = True
            continue
        if in_block:
            # still indented lines
            if line.startswith(' ') or line.startswith('\t'):
                if stripped.startswith('from') or stripped.startswith('import'):
                    if 'typing' not in stripped:
                        to_lift.append(stripped)
                        continue
                    # keep typing imports in block
                # keep other lines inside block
                new_lines.append(line)
                continue
            else:
                in_block = False
        new_lines.append(line)
    if to_lift:
        # find insertion point after initial imports and future imports and comments
        insert_idx = 0
        for i, l in enumerate(new_lines):
            if l.startswith('from __future__') or l.startswith('import') or l.startswith('#'):
                insert_idx = i + 1
        for imp in to_lift:
            new_lines.insert(insert_idx, imp)
            insert_idx += 1
        path.write_text("\n".join(new_lines) + "\n")
        print(f"Updated {path} lifted imports: {to_lift}")
        return True
    return False


def main() -> None:
    """Scan .py files and fix leading spaces before imports."""
    root = pathlib.Path('src')
    for path in root.rglob('*.py'):
        try:
            process_file(path)
        except Exception as e:
            print(f"Skipped {path} due to error: {e}")


if __name__ == '__main__':
    main()
