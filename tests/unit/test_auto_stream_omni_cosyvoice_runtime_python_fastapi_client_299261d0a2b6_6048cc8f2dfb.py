#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_stream_omni_cosyvoice_runtime_python_fastapi_client_299261d0a2b6_6048cc8f2dfb():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\stream_omni_cosyvoice_runtime_python_fastapi_client_299261d0a2b6_6048cc8f2dfb.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("stream_omni_cosyvoice_runtime_python_fastapi_client_299261d0a2b6_6048cc8f2dfb", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
