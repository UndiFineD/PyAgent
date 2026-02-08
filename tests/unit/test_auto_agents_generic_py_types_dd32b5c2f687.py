
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_types_dd32b5c2f687.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AudioSegmentEnd'), 'missing AudioSegmentEnd'
assert hasattr(mod, 'AudioReceiver'), 'missing AudioReceiver'
assert hasattr(mod, 'VideoGenerator'), 'missing VideoGenerator'
