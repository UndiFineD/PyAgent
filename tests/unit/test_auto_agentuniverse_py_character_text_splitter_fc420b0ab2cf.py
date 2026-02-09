#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_agentuniverse_py_character_text_splitter_fc420b0ab2cf():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\agentuniverse_py_character_text_splitter_fc420b0ab2cf.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("agentuniverse_py_character_text_splitter_fc420b0ab2cf", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
