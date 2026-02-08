
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whispers_py_test_log_434aff004b8e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_configure_log'), 'missing test_configure_log'
assert hasattr(mod, 'test_cleanup_log'), 'missing test_cleanup_log'
assert hasattr(mod, 'test_debug'), 'missing test_debug'
