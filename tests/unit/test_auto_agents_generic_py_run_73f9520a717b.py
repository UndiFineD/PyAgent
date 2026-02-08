
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_run_73f9520a717b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'run_dev'), 'missing run_dev'
assert hasattr(mod, '_esc'), 'missing _esc'
assert hasattr(mod, 'run_worker'), 'missing run_worker'
