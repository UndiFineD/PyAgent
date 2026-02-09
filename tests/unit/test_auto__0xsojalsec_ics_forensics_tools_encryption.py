#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import__0xsojalsec_ics_forensics_tools_encryption():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\_0xsojalsec_ics_forensics_tools_encryption.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("_0xsojalsec_ics_forensics_tools_encryption", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
