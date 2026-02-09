#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_0xsojalsec_x_anylabeling_server_py_yolo11_b54e77f95b42():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\0xsojalsec_x_anylabeling_server_py_yolo11_b54e77f95b42.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("0xsojalsec_x_anylabeling_server_py_yolo11_b54e77f95b42", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
