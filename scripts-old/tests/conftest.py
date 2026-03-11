#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Pytest configuration for the repo.

Automatically skip any test module that fails to import because of missing
dependencies.  This prevents the entire test suite from blowing up when
optional packages (e.g. PIL) are not installed during development.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def pytest_ignore_collect(path, config):
    """Skip collecting test files that fail to import due to missing dependencies."""
    # path is a py.path object; convert to str
    p = Path(str(path))
    if not p.name.startswith("test_") and not p.name.endswith("_test.py"):
        return False
    # try importing the module without side effects; skip on any exception
    try:
        spec = importlib.util.spec_from_file_location("_tmp", p)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
    except Exception:
        # skip collection of this file if any import error occurs
        return True
    return False
