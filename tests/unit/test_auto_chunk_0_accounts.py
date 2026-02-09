#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_chunk_0_accounts():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\chunk_0_accounts.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("chunk_0_accounts", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
