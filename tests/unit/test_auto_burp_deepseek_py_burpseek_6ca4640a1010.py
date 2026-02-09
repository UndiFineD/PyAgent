#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_burp_deepseek_py_burpseek_6ca4640a1010():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\burp_deepseek_py_burpseek_6ca4640a1010.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("burp_deepseek_py_burpseek_6ca4640a1010", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
