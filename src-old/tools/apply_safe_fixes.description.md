# apply_safe_fixes

**File**: `src\tools\apply_safe_fixes.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 9 imports  
**Lines**: 146  
**Complexity**: 6 (moderate)

## Overview

Apply safe, automated fixes over extracted candidate files.

Currently implements:
- Replace `yaml.load(` -> `yaml.safe_load(`
- Replace `from yaml import load` -> `from yaml import safe_load as load`

Writes unified diff patches to `.external/patches/` and optionally applies changes when
`--apply` is passed. Re-runs static checks and generated tests after applying fixes.

## Functions (6)

### `find_py_files(target)`

### `transform_text(text)`

### `remove_top_level_asserts(text)`

### `write_patch(orig_path, orig_text, new_text, patch_dir, base_dir)`

### `apply_fixes(apply, target_dir, patch_dir)`

### `main(argv)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `argparse`
- `ast`
- `difflib`
- `pathlib.Path`
- `re`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
