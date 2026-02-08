
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_models_dbc0d07bf9d8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EnvStatus'), 'missing EnvStatus'
assert hasattr(mod, 'Address'), 'missing Address'
assert hasattr(mod, 'Env'), 'missing Env'
assert hasattr(mod, 'EnvInstance'), 'missing EnvInstance'
assert hasattr(mod, 'EnvInstanceCreateRequest'), 'missing EnvInstanceCreateRequest'
assert hasattr(mod, 'EnvInstanceListResponse'), 'missing EnvInstanceListResponse'
assert hasattr(mod, 'APIResponse'), 'missing APIResponse'
assert hasattr(mod, 'APIError'), 'missing APIError'
