
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_tts_fallback_1563fc435979.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FallbackAdapterTester'), 'missing FallbackAdapterTester'
assert hasattr(mod, 'test_tts_fallback'), 'missing test_tts_fallback'
assert hasattr(mod, 'test_no_audio'), 'missing test_no_audio'
assert hasattr(mod, 'test_tts_stream_fallback'), 'missing test_tts_stream_fallback'
assert hasattr(mod, 'test_tts_recover'), 'missing test_tts_recover'
assert hasattr(mod, 'test_audio_resampled'), 'missing test_audio_resampled'
assert hasattr(mod, 'test_timeout'), 'missing test_timeout'
