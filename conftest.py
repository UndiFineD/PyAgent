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
# We *used* to insert the ``src`` folder onto ``sys.path`` so that
# ``import infrastructure`` would work during ad-hoc experimentation.
#
# The package hierarchy in this repository is deliberately rooted at
# ``src`` (i.e. modules are imported as ``src.foo``).  Having both the
# workspace root AND the ``src`` directory on ``sys.path`` creates the
# possibility of loading the same file under two different module names
# (``infrastructure.foo`` vs ``src.infrastructure.foo``) which leads to
# the “partially initialized module” errors we observed earlier.  Simply
# leaving the workspace root on ``sys.path`` is sufficient for the
# canonical imports, so we no longer need this helper.
#
# SRC_DIR = ROOT / "src"
# if str(SRC_DIR) not in sys.path:
#     sys.path.insert(0, str(SRC_DIR))

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
        """Patched version of ``spec_from_file_location`` that infers both the
        canonical module name and the package.

        Tests load modules using a dummy name (``_mod_under_test``) so that the
        resulting module object does not collide with any existing entry in
        ``sys.modules``.  That strategy is convenient until the module under
        test itself performs imports from sibling packages; the import
        machinery then tries to load a second copy of the same file under the
        real package path, leading to ``ImportError: cannot import name ...
        from partially initialized module`` when circular references exist.

        By assigning the spec a proper name derived from the file path we
        guarantee that the module is registered under its canonical package
        path.  Combined with our ``module_from_spec`` patch (which inserts the
        module into ``sys.modules`` immediately) this ensures a single Python
        object per file and prevents spurious import errors.
        """
        spec = self._orig_spec(name, location, *args, **kwargs)
        if spec and spec.loader:
            # we keep ``spec.name`` unchanged; rewriting it previously caused
            # the loader instance itself to carry the wrong name, leading to
            # ImportError later when Python tried to import the canonical module
            # name.  Instead we update the loader's ``name`` attribute and perform
            # aliasing in ``_patched_module``.
            #
            # ``__package__`` is still set because relative imports rely on it.

            pkg = self._infer_package(spec.origin)
            if pkg is not None:
                spec.__package__ = pkg
            # If the caller used the dummy placeholder we also want the loader to
            # advertise the canonical name.  ``SourceFileLoader`` checks its
            # ``name`` attribute when ``get_code`` is invoked, which explains the
            # ImportError we saw earlier.  Overwriting the loader's name here is a
            # lightweight way to make it accept imports for the real package.
            if name == "_mod_under_test" and spec.origin:
                try:
                    p = Path(spec.origin).resolve()
                    root = ROOT / "src"
                    if root in p.parents or p == root:
                        rel = p.relative_to(root)
                        canon = "src." + ".".join(rel.with_suffix("").parts)
                        spec.loader.name = canon
                except Exception:
                    pass
        return spec

    def _patched_module(self, spec):
        """Patched version of ``module_from_spec`` that sets ``__package__`` and
        registers the newly created module in ``sys.modules`` immediately.

        When tests call ``spec_from_file_location('_mod_under_test', path)`` the
        returned specification carries a meaningless name.  We must ensure the
        executed module is visible under *both* that placeholder and the real
        package name; otherwise sibling imports will create a second module
        object and circular dependencies blow up.  Additionally we update the
        module's ``__name__`` so dataclasses, logging, and other introspection
        code see the correct package path.
        """
        mod = self._orig_module(spec)
        mod.__package__ = getattr(spec, "__package__", "") or ""
        import sys
        # register under the spec name first
        sys.modules[spec.name] = mod
        # if this is the dummy placeholder we also register under the canonical
        # import path and rename the module object accordingly
        if spec.name == "_mod_under_test" and spec.origin:
            try:
                p = Path(spec.origin).resolve()
                root = ROOT / "src"
                if root in p.parents or p == root:
                    rel = p.relative_to(root)
                    canon = "src." + ".".join(rel.with_suffix("" ).parts)
                    sys.modules[canon] = mod
                    mod.__name__ = canon
            except Exception:
                pass
        return mod

    def _infer_package(self, origin: str) -> str | None:
        """Infers the package name from the file path of the module being imported."""
        try:
            p = Path(origin).resolve()
            parts = list(p.parts)
            if "src" in parts:
                idx = parts.index("src")
                # keep the leading "src." so that the package matches the
                # canonical import path used throughout the repository.
                pkg = ".".join(parts[idx : -1])
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
        """Restores the original Path.write_text and built-in open functions."""
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
        """Initializes the StarImportManager with the root directory to scan for test files."""
        self.tests_root = root / "src"

    def collect_modules(self) -> set[str]:
        """Scans test files for `from X import *` patterns and collects the module names."""
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
        """Pre-imports all modules collected from test files to ensure they are available for star imports."""
        mods = self.collect_modules()
        logger = logging.getLogger("pytest-shim")
        for m in sorted(mods):
            try:
                importlib.import_module(m)
            except (ImportError, ModuleNotFoundError, ValueError) as e:
                logger.debug("pytest-shim: failed to import %s: %s", m, e)

    def inject_globals(self, item: "pytest.Item") -> None:
        """Injects names from pre-imported modules into the test's global namespace if it contains star imports."""
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
        """Logs the attempt to import a module for star import, including whether the target globals already contain a key from that module."""
        try:
            debug_file = ROOT / "pytest_shim_debug.log"
            with debug_file.open("a", encoding="utf-8") as fh:
                nodeid = getattr(item, "nodeid", "<unknown>")
                fh.write(f"{nodeid} importing {module_name} exists_before={('ArchiveIntelligence' in (target_globals or {}))}\n")
        except OSError:
            pass

    def _make_shim_dir(self, tg: dict[str, object]) -> Callable[[object | None], list[str]]:
        """Creates a shim for the `dir` function that returns the keys of the target globals when called with None, and otherwise behaves like the normal `dir` function."""
        def _shim_dir(obj: object = None) -> list[str]:
            if obj is None:
                return sorted(list(tg.keys()))
            return builtins.dir(obj)
        return _shim_dir


# ---------------------------------------------------------------------------
# session hook manager
# ---------------------------------------------------------------------------

class SessionManager:
    """Manages pytest session hooks for setup and teardown, including file write tracking and star import support.
    """

    def __init__(self, root: Path):
        """Initializes the SessionManager with the root directory and creates a StarImportManager."""
        self.root = root
        self.star_imports = StarImportManager(root)

    def session_start(self, session: object) -> None:
        """Runs at the start of the pytest session, applying the WriteTracker and pre-importing star import modules."""
        del session  # unused

        with WriteTracker(self.root):
            logging.getLogger("pytest-shim").debug("running leading-import fixer")
            try:
                subprocess.run([sys.executable, "scripts/fix_leading_imports.py"], check=True)
            except Exception as exc:  # pragma: no cover
                logging.getLogger("pytest-shim").warning("import fixer invocation failed: %s", exc)

        self.star_imports.preimport()

    def runtest_setup(self, item: "pytest.Item") -> None:
        """Runs before each test, injecting star import names into the test's global namespace."""
        self.star_imports.inject_globals(item)

    def session_finish(self, session: object, exitstatus: int) -> None:
        """Runs at the end of the pytest session, checking for any file writes that occurred during testing and logging them."""
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
    """Pytest hook that runs at the start of the session, delegating to the SessionManager."""
    _mgr.session_start(session)


def pytest_runtest_setup(item):
    """Pytest hook that runs before each test, delegating to the SessionManager."""
    _mgr.runtest_setup(item)


def pytest_sessionfinish(session, exitstatus):
    """Pytest hook that runs at the end of the session, delegating to the SessionManager."""
    _mgr.session_finish(session, exitstatus)

