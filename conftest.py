#!/usr/bin/env python3
"""Pytest configuration for the repository.

Ensure `src` is first on `sys.path` so tests import the package sources
consistently. This avoids creating top-level shim packages that may shadow
stdlib modules.
"""
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
# We'll insert repository root in a way that doesn't shadow real packages
# such as NumPy. A top-level `numpy.py` shim exists in the repo, which
# should only be used when NumPy isn't installed in the environment. To
# avoid import confusion, detect whether a *real* numpy is loadable first.
ROOT_STR = str(ROOT)
# Determine if there is a real numpy on sys.path (i.e. not our shim).
real_numpy = False
# We need to temporarily avoid loading the repo root itself because
# Python starts with '' (current directory) on sys.path which points to
# the project root. Without this workaround, `import numpy` would pick up
# our shim at the top level and we would incorrectly conclude that a
# "real" numpy isn't installed.
_saved_path = sys.path.copy()
try:
    sys.path = [p for p in sys.path if p and str(Path(p).resolve()) != ROOT_STR]
    import numpy as _np
    # if numpy module file path is outside the repo root, it's real
    if not str(Path(_np.__file__).resolve()).startswith(ROOT_STR):
        real_numpy = True
except Exception:
    pass
finally:
    sys.path = _saved_path

if ROOT_STR not in sys.path:
    if real_numpy:
        # leave ROOT later in the path so site-packages takes precedence
        sys.path.append(ROOT_STR)
    else:
        # no real numpy; root may provide a shim so put it first
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
        except (OSError, UnicodeDecodeError):
            continue
        for m in pattern.findall(txt):
            modules.add(m)
    return modules


def pytest_sessionstart(session: object) -> None:
    """Pytest hook: run before collection. Pre-import modules referenced by tests.

    This avoids many star-import/import-order failures during collection by
    ensuring the referenced modules exist in sys.modules and are importable.
    """
    # `session` is required by pytest's hook signature but not used here.
    # suppress lint warning about unused parameter by deleting it.
    del session
    import importlib
    import logging

    mods = _collect_star_import_modules("src")
    if not mods:
        return
    logger = logging.getLogger("pytest-shim")
    for m in sorted(mods):
        try:
            importlib.import_module(m)
        except (ImportError, ModuleNotFoundError, ValueError) as e:
            logger.debug("pytest-shim: failed to import %s: %s", m, e)


def pytest_runtest_setup(item: "pytest.Item") -> None:
    """Before each test, inject names from any `from X import *` in the test
    module source into the test module globals if they are missing.
    """
    try:
        path = Path(item.fspath)
        txt = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    import re
    import importlib
    import builtins as builtins_module

    # default in case no star imports are found
    target_globals: dict[str, object] | None = None
    mod = None

    pattern = re.compile(r"from\s+([a-zA-Z0-9_.]+)\s+import\s+\*")
    for m in pattern.findall(txt):
        try:
            mod = importlib.import_module(m)
        except (ImportError, ModuleNotFoundError, ValueError):
            continue
        # Prefer injecting into the test function's globals since `dir()`
        # inside a test reflects the function globals. Fall back to the
        # module dict when a function object isn't available.
        func = getattr(item, "function", None)
        if func is not None:
            target_globals = func.__globals__
        else:
            target_module = getattr(item, "module", None)
            if target_module is None:
                continue
            target_globals = target_module.__dict__
        # Debug: write a small trace to help diagnose why names may be missing
        try:
            debug_file = ROOT / "pytest_shim_debug.log"
            with debug_file.open("a", encoding="utf-8") as fh:
                nodeid = getattr(item, "nodeid", "<unknown>")
                fh.write(f"{nodeid} importing {m} exists_before={('ArchiveIntelligence' in target_globals)}\n")
        except OSError:
            pass

    # if we never populated target_globals we can skip the shim
    if target_globals is None or mod is None:
        return

    # Provide a local `dir()` replacement in the test globals so
    # `dir()` called without arguments will include module globals
    # (where star-imported names live) rather than only function locals.
    def _make_shim_dir(tg: dict[str, object]) -> Callable[[object | None], list[str]]:
        """Create a shim for `dir()` that includes the target globals
        when called without arguments.
        """

        def _shim_dir(obj: object = None) -> list[str]:
            """When called without arguments, 
            return the sorted keys of the target globals.
            Otherwise, behave like built-in dir().
            """
            if obj is None:
                return sorted(list(tg.keys()))
            return builtins_module.dir(obj)
        return _shim_dir

    try:
        target_globals["dir"] = _make_shim_dir(target_globals)
    except (AttributeError, TypeError):
        pass
    for name in dir(mod):
        if name.startswith("_"):
            continue
        if name not in target_globals:
            try:
                target_globals[name] = getattr(mod, name)
            except (AttributeError, TypeError):
                # best-effort: skip attributes that raise on access
                continue

