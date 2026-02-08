
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_interval_c85e8c93e37c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_finish_fut'), 'missing _finish_fut'
assert hasattr(mod, 'Interval'), 'missing Interval'
assert hasattr(mod, 'interval'), 'missing interval'
