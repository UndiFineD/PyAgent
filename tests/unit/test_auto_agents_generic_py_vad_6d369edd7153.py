
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_vad_6d369edd7153.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'VADEventType'), 'missing VADEventType'
assert hasattr(mod, 'VADEvent'), 'missing VADEvent'
assert hasattr(mod, 'VADCapabilities'), 'missing VADCapabilities'
assert hasattr(mod, 'VAD'), 'missing VAD'
assert hasattr(mod, 'VADStream'), 'missing VADStream'
