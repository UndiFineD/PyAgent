
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_errors_152fc4e44859.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AcontextError'), 'missing AcontextError'
assert hasattr(mod, 'APIError'), 'missing APIError'
assert hasattr(mod, 'TransportError'), 'missing TransportError'
