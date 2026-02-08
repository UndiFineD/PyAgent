
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_strategies_e252f9eb457f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DefaultAuthorizationStrategy'), 'missing DefaultAuthorizationStrategy'
assert hasattr(mod, 'RoleBasedAuthorizationStrategy'), 'missing RoleBasedAuthorizationStrategy'
assert hasattr(mod, 'CustomAuthorizationStrategy'), 'missing CustomAuthorizationStrategy'
