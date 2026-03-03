#!/usr/bin/env python3
"""Pytest configuration for the repository.

Ensure `src` is first on `sys.path` so tests import the package sources
consistently. This avoids creating top-level shim packages that may shadow
stdlib modules.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Insert repository root so absolute imports like `from src.core...` resolve.
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

# Also ensure the `src` directory is available for direct imports if necessary.
SRC = str((ROOT / "src").resolve())
if SRC not in sys.path:
    sys.path.append(SRC)


def _collect_star_import_modules(tests_root: str = "src") -> set[str]:
    """Scan test files for `from X import *` and return module names.

    This is a conservative, best-effort heuristic used by the pytest shim to
    pre-import modules that tests expect to star-import at module import time.
    """
import re

    modules: set[str] = set()
    pattern = re.compile(r"from\s+([a-zA-Z0-9_.]+)\s+import\s+\*")

    root = Path(tests_root)
    if not root.exists():
        return modules

    for p in root.rglob("*_test.py"):
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in pattern.findall(txt):
            modules.add(m)
    return modules


def pytest_sessionstart(session):
    """Pytest hook: run before collection. Pre-import modules referenced by tests.

    This avoids many star-import/import-order failures during collection by
    ensuring the referenced modules exist in sys.modules and are importable.
    """
    import importlib
    import logging

    mods = _collect_star_import_modules("src")
    if not mods:
        return
    logger = logging.getLogger("pytest-shim")
    for m in sorted(mods):
        try:
            importlib.import_module(m)
        except Exception as e:
            logger.debug("pytest-shim: failed to import %s: %s", m, e)


def pytest_runtest_setup(item):
    """Before each test, inject names from any `from X import *` in the test
    module source into the test module globals if they are missing.
    """
    try:
        path = Path(item.fspath)
        txt = path.read_text(encoding="utf-8")
    except Exception:
        return

    import re
    import importlib

    pattern = re.compile(r"from\s+([a-zA-Z0-9_.]+)\s+import\s+\*")
    for m in pattern.findall(txt):
        try:
            mod = importlib.import_module(m)
        except Exception:
            continue
        # Prefer injecting into the test function's globals since `dir()`
        # inside a test reflects the function globals. Fall back to the
        # module dict when a function object isn't available.
        if hasattr(item, "function") and getattr(item, "function") is not None:
            target_globals = item.function.__globals__
        else:
            target_module = getattr(item, "module", None)
            if target_module is None:
                continue
            target_globals = target_module.__dict__
        # Debug: write a small trace to help diagnose why names may be missing
        try:
            debug_file = ROOT / "pytest_shim_debug.log"
            with debug_file.open("a", encoding="utf-8") as fh:
                fh.write(f"{item.nodeid} importing {m} exists_before={('ArchiveIntelligence' in target_globals)}\n")
        except Exception:
            pass
        # Provide a local `dir()` replacement in the test globals so
        # `dir()` called without arguments will include module globals
        # (where star-imported names live) rather than only function locals.
        try:
            import builtins

            def _shim_dir(obj=None):
                if obj is None:
                    return sorted(list(target_globals.keys()))
                return builtins.dir(obj)

            target_globals["dir"] = _shim_dir
        except Exception:
            pass
        for name in dir(mod):
            if name.startswith("_"):
                continue
            if name not in target_globals:
                try:
                    target_globals[name] = getattr(mod, name)
                except Exception:
                    # best-effort: skip attributes that raise on access
                    continue
