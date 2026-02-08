
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_stt_fallback_29928f86065f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FallbackAdapterTester'), 'missing FallbackAdapterTester'
assert hasattr(mod, 'test_stt_fallback'), 'missing test_stt_fallback'
assert hasattr(mod, 'test_stt_stream_fallback'), 'missing test_stt_stream_fallback'
assert hasattr(mod, 'test_stt_recover'), 'missing test_stt_recover'
