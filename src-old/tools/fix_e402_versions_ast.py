"""LLM_CONTEXT_START

## Source: src-old/tools/fix_e402_versions_ast.description.md

# fix_e402_versions_ast

**File**: `src\tools\fix_e402_versions_ast.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 2 imports  
**Lines**: 87  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for fix_e402_versions_ast.

## Functions (2)

### `fix_file(filepath)`

### `main()`

## Dependencies

**Imports** (2):
- `ast`
- `os`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_e402_versions_ast.improvements.md

# Improvements for fix_e402_versions_ast

**File**: `src\tools\fix_e402_versions_ast.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 87 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_e402_versions_ast_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import ast
import os


def fix_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
    except Exception:
        return False

    # Find the version assignment and import
    version_import_node = None
    version_assign_node = None
    last_import_node = None

    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "src.core.base.version":
            for alias in node.names:
                if alias.name == "VERSION":
                    version_import_node = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__version__":
                    if isinstance(node.value, ast.Name) and node.value.id == "VERSION":
                        version_assign_node = node

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_node = node

    if not (version_import_node and version_assign_node and last_import_node):
        return False

    # If the version assign is already after all imports (or is the last import block), we are good
    # But wait, version_assign_node is an Assign, so it must be after all imports to satisfy E402.

    if version_assign_node.lineno > last_import_node.lineno:
        # Check if there are other imports after it (though last_import_node should cover this)
        return False

    # Perform the move
    lines = content.splitlines()

    # Remove nodes in reverse order to keep indices valid if we used them,
    # but we'll just reconstruct the file.
    # Actually, it's easier to just remove the specific lines.

    v_import_line = version_import_node.lineno - 1
    v_assign_line = version_assign_node.lineno - 1

    # Get the lines to move
    # Note: lineno starts at 1
    import_line_text = lines[v_import_line]
    assign_line_text = lines[v_assign_line]

    # Remove them
    # Be careful not to remove the wrong lines if multiple things are on the same line
    lines[v_import_line] = ""
    lines[v_assign_line] = ""

    # Find last import line index
    last_idx = (
        last_import_node.end_lineno
        if hasattr(last_import_node, "end_lineno")
        else last_import_node.lineno
    )

    # Insert them AFTER the last import
    # Index is 0-based, so last_idx is the line AFTER the last import line.
    lines.insert(last_idx, import_line_text)
    lines.insert(last_idx + 1, assign_line_text)

    # Clean up and join
    new_content = "\n".join(line for line in lines if line is not None)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


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
