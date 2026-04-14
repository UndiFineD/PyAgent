"""Orchestration package for GitHub agent plugins.

Creating this file makes the directory a Python package so relative
imports like `from .backend import PostgresBackend` resolve for
type-checkers and runtime imports.
"""

import importlib

# Import submodules into package globals so `from . import backend` and
# `from .backend import PostgresBackend` resolve for type-checkers and
# linters that inspect `__all__`.
for _mod in ("backend", "fleet", "fleetmanager", "intent_decomposer"):
    try:
        globals()[_mod] = importlib.import_module(f"{__package__}.{_mod}")
    except Exception:
        globals()[_mod] = None

__all__ = ["backend", "fleet", "fleetmanager", "intent_decomposer"]
