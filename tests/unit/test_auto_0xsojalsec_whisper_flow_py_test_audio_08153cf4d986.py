
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisper_flow_py_test_audio_08153cf4d986.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_capture_mic'), 'missing test_capture_mic'
assert hasattr(mod, 'test_is_silent'), 'missing test_is_silent'
assert hasattr(mod, 'test_play_audio'), 'missing test_play_audio'
