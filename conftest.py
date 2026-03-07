#!/usr/bin/env python3
"""Pytest configuration for the repository.

This module defines a small object-oriented framework for our custom
`pytest` shims.  Each responsibility is encapsulated in a class and the
public functions at the bottom simply delegate to a single manager
instance.  The goal is maintainability – the previous procedural file
grew unwieldy and produced flake8 errors; the new design avoids global
state and clarifies intent.
"""

import sys
import logging
import importlib
import traceback
import builtins
import subprocess
import re
from pathlib import Path
from collections.abc import Callable

# root directory of repository, used by various helpers
ROOT = Path(__file__).resolve().parent

import pytest


# ---------------------------------------------------------------------------
# importlib patching
# ---------------------------------------------------------------------------

class ImportlibPatcher:
    """Handles the `spec_from_file_location` and `module_from_spec`
    monkey‑patches used to provide sensible ``__package__`` values.
    """

    def __init__(self) -> None:
        """Saves original functions for later use."""
        self._orig_spec = importlib.util.spec_from_file_location
        self._orig_module = importlib.util.module_from_spec

    def patch(self) -> None:
        """Applies the monkey‑patches to `importlib.util` functions.
        """
        importlib.util.spec_from_file_location = self._patched_spec
        importlib.util.module_from_spec = self._patched_module

    def _patched_spec(self, name, location, *args, **kwargs):
        """Patched version of `spec_from_file_location` that infers and sets"""
        spec = self._orig_spec(name, location, *args, **kwargs)
        if spec and spec.loader:
            pkg = self._infer_package(spec.origin)
            if pkg is not None:
                spec.__package__ = pkg
        return spec

    def _patched_module(self, spec):
        """Patched version of `module_from_spec` that ensures the created module has"""
        mod = self._orig_module(spec)
        mod.__package__ = getattr(spec, "__package__", "") or ""
        return mod

    def _infer_package(self, origin: str) -> str | None:
        """Infers the package name from the file path of the module being imported."""
        try:
            p = Path(origin).resolve()
            parts = list(p.parts)
            if "src" in parts:
                idx = parts.index("src")
                pkg = ".".join(parts[idx + 1 : -1])
                if pkg.startswith("src."):
                    pkg = pkg[len("src.") :]
                return pkg
        except Exception:
            pass
        return None


# apply immediately at import time
ImportlibPatcher().patch()


# ---------------------------------------------------------------------------
# instrumentation utilities
# ---------------------------------------------------------------------------

class WriteTracker:
    """Logs any file writes that occur during a test session."""

    def __init__(self, root: Path) -> None:
        """Initializes the WriteTracker with a log file path and saves original functions."""
        self.log_path = root / "pytest_shim_writes.log"
        self._orig_write = Path.write_text
        self._orig_open = builtins.open

    def __enter__(self):
        """Monkey-patches Path.write_text and built-in open to log file writes."""
        def logged_write(self, data, encoding="utf-8"):
            """Logged version of Path.write_text that records the file being written and a stack trace."""
            try:
                with self.log_path.open("a", encoding="utf-8") as fh:
                    fh.write(f"WRITE {self!r}\n")
                    fh.write(traceback.format_stack(limit=5)[0])
            except OSError:
                pass
            return self._orig_write(self, data, encoding=encoding)

        def logged_open(file, mode="r", *args, **kwargs):
            """Logged version of built-in open that records files opened in write modes and a stack trace."""
            result = self._orig_open(file, mode, *args, **kwargs)
            if any(m in mode for m in ("w", "a", "+", "x")):
                try:
                    with self.log_path.open("a", encoding="utf-8") as fh:
                        fh.write(f"OPEN {file!r} mode={mode}\n")
                        fh.write(traceback.format_stack(limit=5)[0])
                except OSError:
                    pass
            return result

        Path.write_text = logged_write
        builtins.open = logged_open

    def __exit__(self, exc_type, exc, tb):
        Path.write_text = self._orig_write
        builtins.open = self._orig_open


# ---------------------------------------------------------------------------
# star-import support
# ---------------------------------------------------------------------------

class StarImportManager:
    """Pre‑imports modules referenced by ``from X import *`` in tests and
    injects names during runtest setup.
    """

    pattern = re.compile(r"from\s+([a-zA-Z0-9_.]+)\s+import\s+\*")

    def __init__(self, root: Path):
        self.tests_root = root / "src"

    def collect_modules(self) -> set[str]:
        modules: set[str] = set()
        if not self.tests_root.exists():
            return modules
        for p in self.tests_root.rglob("*_test.py"):
            try:
                txt = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for m in self.pattern.findall(txt):
                modules.add(m)
        return modules

    def preimport(self) -> None:
        mods = self.collect_modules()
        logger = logging.getLogger("pytest-shim")
        for m in sorted(mods):
            try:
                importlib.import_module(m)
            except (ImportError, ModuleNotFoundError, ValueError) as e:
                logger.debug("pytest-shim: failed to import %s: %s", m, e)

    def inject_globals(self, item: "pytest.Item") -> None:
        try:
            path = Path(item.fspath)
            txt = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return

        target_globals = None
        mod = None
        for m in self.pattern.findall(txt):
            try:
                mod = importlib.import_module(m)
            except (ImportError, ModuleNotFoundError, ValueError):
                continue
            func = getattr(item, "function", None)
            if func is not None:
                target_globals = func.__globals__
            else:
                target_module = getattr(item, "module", None)
                if target_module is None:
                    continue
                target_globals = target_module.__dict__
            self._debug_log(item, m, target_globals)
        if target_globals is None or mod is None:
            return
        target_globals["dir"] = self._make_shim_dir(target_globals)
        for name in dir(mod):
            if name.startswith("_"):
                continue
            if name not in target_globals:
                try:
                    target_globals[name] = getattr(mod, name)
                except (AttributeError, TypeError):
                    continue

    def _debug_log(self, item, module_name, target_globals):
        try:
            debug_file = ROOT / "pytest_shim_debug.log"
            with debug_file.open("a", encoding="utf-8") as fh:
                nodeid = getattr(item, "nodeid", "<unknown>")
                fh.write(f"{nodeid} importing {module_name} exists_before={('ArchiveIntelligence' in (target_globals or {}))}\n")
        except OSError:
            pass

    def _make_shim_dir(self, tg: dict[str, object]) -> Callable[[object | None], list[str]]:
        def _shim_dir(obj: object = None) -> list[str]:
            if obj is None:
                return sorted(list(tg.keys()))
            return builtins.dir(obj)
        return _shim_dir


# ---------------------------------------------------------------------------
# session hook manager
# ---------------------------------------------------------------------------

class SessionManager:
    def __init__(self, root: Path):
        self.root = root
        self.star_imports = StarImportManager(root)

    def session_start(self, session: object) -> None:
        del session  # unused

        with WriteTracker(self.root):
            logging.getLogger("pytest-shim").debug("running leading-import fixer")
            try:
                subprocess.run([sys.executable, "scripts/fix_leading_imports.py"], check=True)
            except Exception as exc:  # pragma: no cover
                logging.getLogger("pytest-shim").warning("import fixer invocation failed: %s", exc)

        self.star_imports.preimport()

    def runtest_setup(self, item: "pytest.Item") -> None:
        self.star_imports.inject_globals(item)

    def session_finish(self, session: object, exitstatus: int) -> None:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            )
            if result.stdout.strip():
                print("\nERROR: tests altered the workspace files:\n")
                print(result.stdout)
                session.exitstatus = 1
        except Exception:
            pass


# instantiate manager and expose hooks
_mgr = SessionManager(Path(__file__).resolve().parent)

def pytest_sessionstart(session):
    _mgr.session_start(session)


def pytest_runtest_setup(item):
    _mgr.runtest_setup(item)


def pytest_sessionfinish(session, exitstatus):
    _mgr.session_finish(session, exitstatus)

