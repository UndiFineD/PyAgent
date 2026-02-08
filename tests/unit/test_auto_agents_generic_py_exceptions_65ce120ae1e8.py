
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_exceptions_65ce120ae1e8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AssignmentTimeoutError'), 'missing AssignmentTimeoutError'
assert hasattr(mod, 'APIError'), 'missing APIError'
assert hasattr(mod, 'APIStatusError'), 'missing APIStatusError'
assert hasattr(mod, 'APIConnectionError'), 'missing APIConnectionError'
assert hasattr(mod, 'APITimeoutError'), 'missing APITimeoutError'
