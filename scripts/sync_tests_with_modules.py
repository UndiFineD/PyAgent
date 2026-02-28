#!/usr/bin/env python3
"""Scan src/ for Python modules and sync corresponding *_test.py files.

This creates/overwrites a simple test file next to each module that
verifies the module can be imported and that its public functions/classes
exist. It avoids executing the module at import time by loading from file
via importlib.util with the module file path (tests will still execute
top-level code when loading; review modules with heavy side-effects).

Run from repo root: python -m scripts.sync_tests_with_modules or
python scripts/sync_tests_with_modules.py
"""
from __future__ import annotations

import ast
import pathlib
import sys
from typing import List

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def public_names_from_file(path: pathlib.Path) -> List[str]:
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        tree = ast.parse(src)
    except Exception:
        return []
    names: List[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            # look for __all__ or simple names
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    # try to evaluate simple literal __all__ lists
                    try:
                        val = ast.literal_eval(node.value)
                        if isinstance(val, (list, tuple)):
                            for it in val:
                                if isinstance(it, str) and not it.startswith("_"):
                                    names.append(it)
                    except Exception:
                        pass
    # de-duplicate preserving order
    out: List[str] = []
    for n in names:
        if n not in out:
            out.append(n)
    return out


TEST_TEMPLATE = """# Auto-synced test for {module_name}
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "{module_file}"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
{asserts}
"""


def make_asserts(names: List[str]) -> str:
    if not names:
        return "    assert mod is not None\n"
    lines = []
    for n in names:
        safe = n.replace('"', '\\"')
        lines.append(f'    assert hasattr(mod, "{safe}"), "{safe} missing"')
    return "\n".join(lines) + "\n"


def process_module(py_path: pathlib.Path) -> bool:
    rel = py_path.relative_to(SRC)
    module_file = py_path.name
    module_name = str(rel).replace("\\", "/")
    names = public_names_from_file(py_path)
    asserts = make_asserts(names)
    content = TEST_TEMPLATE.format(module_name=module_name, module_file=module_file, asserts=asserts)
    test_path = py_path.with_name(py_path.stem + "_test.py")
    try:
        test_path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def main() -> int:
    count = 0
    updated = 0
    for p in SRC.rglob("*.py"):
        # skip tests and __init__ files
        if p.name.endswith("_test.py"):
            continue
        if p.name.startswith("__init__"):
            continue
        count += 1
        ok = process_module(p)
        if ok:
            updated += 1
    print(f"Processed {count} modules; updated {updated} test files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
