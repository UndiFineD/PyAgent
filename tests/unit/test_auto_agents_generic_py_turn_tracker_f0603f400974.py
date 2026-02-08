
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_turn_tracker_f0603f400974.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_Phase'), 'missing _Phase'
assert hasattr(mod, '_Turn'), 'missing _Turn'
assert hasattr(mod, '_TurnTracker'), 'missing _TurnTracker'
assert hasattr(mod, '_classify'), 'missing _classify'
