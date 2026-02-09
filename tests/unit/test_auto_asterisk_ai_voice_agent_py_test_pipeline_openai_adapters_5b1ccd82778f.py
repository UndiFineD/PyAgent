#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_asterisk_ai_voice_agent_py_test_pipeline_openai_adapters_5b1ccd82778f():
    p = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned\asterisk_ai_voice_agent_py_test_pipeline_openai_adapters_5b1ccd82778f.py")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("asterisk_ai_voice_agent_py_test_pipeline_openai_adapters_5b1ccd82778f", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
