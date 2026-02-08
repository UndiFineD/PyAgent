
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_xsssniper_py_winterm_9d7cecf05b6d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WinColor'), 'missing WinColor'
assert hasattr(mod, 'WinStyle'), 'missing WinStyle'
assert hasattr(mod, 'WinTerm'), 'missing WinTerm'
