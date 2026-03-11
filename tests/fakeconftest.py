#!/usr/bin/env python
"""Test configuration for fake tests to ensure test infrastructure is working."""
import os
import sys

# ensure `src` directory is on the import path for tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
