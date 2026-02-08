
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_utils_29b3fd578dbc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'find_micro_track_id'), 'missing find_micro_track_id'
assert hasattr(mod, 'segment_uuid'), 'missing segment_uuid'
assert hasattr(mod, 'speech_uuid'), 'missing speech_uuid'
