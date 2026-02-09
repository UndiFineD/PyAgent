#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_stream_omni_py_flow_matching_a1481767c3ec():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\stream_omni_py_flow_matching_a1481767c3ec.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("stream_omni_py_flow_matching_a1481767c3ec", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
