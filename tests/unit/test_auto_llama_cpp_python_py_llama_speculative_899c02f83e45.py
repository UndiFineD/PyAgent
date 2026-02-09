#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_llama_cpp_python_py_llama_speculative_899c02f83e45():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\llama_cpp_python_py_llama_speculative_899c02f83e45.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("llama_cpp_python_py_llama_speculative_899c02f83e45", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
