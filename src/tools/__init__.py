#!/usr/bin/env python3
"""Tools package.

Importing this package will register all tools via `tool_registry`. Each tool module
calls `register_tool()` during import.

The recommended entrypoint is `python -m src.tools` (see `__main__.py`).
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path

# Import all modules in this package so they can register themselves.
# This avoids requiring users to explicitly import each tool module.

# Avoid altering __path__; the import system already sets it correctly for this package.
# (The prior implementation used __import__(__name__).__path__, which resolves to the
# top-level `src` package and breaks submodule imports like `src.tools.__main__`.)

for finder, name, ispkg in pkgutil.iter_modules(__path__):
    if ispkg:
        continue
    # Skip modules that are not intended as tools (e.g. internal helpers)
    # Also skip the package __main__.py as it is executed only when run as a module.
    if name in {"tool_registry", "__main__"}:
        continue
    try:
        importlib.import_module(f"{__name__}.{name}")
    except Exception:
        # If a tool fails to import, do not crash on package import.
        # The tool may have optional dependencies, so we ignore failures here.
        pass
