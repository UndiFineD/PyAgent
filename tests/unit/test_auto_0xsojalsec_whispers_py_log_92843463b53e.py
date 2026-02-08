
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whispers_py_log_92843463b53e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'configure_log'), 'missing configure_log'
assert hasattr(mod, 'cleanup_log'), 'missing cleanup_log'
assert hasattr(mod, 'debug'), 'missing debug'
