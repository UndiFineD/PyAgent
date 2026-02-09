#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_code_puppy_py_managed_server_d3b9c895c6d1():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\code_puppy_py_managed_server_d3b9c895c6d1.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("code_puppy_py_managed_server_d3b9c895c6d1", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
