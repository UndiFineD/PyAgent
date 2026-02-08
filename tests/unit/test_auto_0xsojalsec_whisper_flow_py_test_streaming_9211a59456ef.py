
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisper_flow_py_test_streaming_9211a59456ef.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_simple'), 'missing test_simple'
assert hasattr(mod, 'test_transcribe_streaming'), 'missing test_transcribe_streaming'
assert hasattr(mod, 'test_streaming'), 'missing test_streaming'
assert hasattr(mod, 'test_ws'), 'missing test_ws'
