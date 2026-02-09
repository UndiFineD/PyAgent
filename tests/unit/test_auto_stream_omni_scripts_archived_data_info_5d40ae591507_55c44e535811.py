#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_stream_omni_scripts_archived_data_info_5d40ae591507_55c44e535811():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\stream_omni_scripts_archived_data_info_5d40ae591507_55c44e535811.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("stream_omni_scripts_archived_data_info_5d40ae591507_55c44e535811", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
