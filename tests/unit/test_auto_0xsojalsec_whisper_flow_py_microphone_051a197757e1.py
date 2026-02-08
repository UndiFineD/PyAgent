
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisper_flow_py_microphone_051a197757e1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'capture_audio'), 'missing capture_audio'
assert hasattr(mod, 'play_audio'), 'missing play_audio'
assert hasattr(mod, 'is_silent'), 'missing is_silent'
