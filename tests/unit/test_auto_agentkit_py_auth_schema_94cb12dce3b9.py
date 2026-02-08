
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_auth_schema_94cb12dce3b9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AccountSchema'), 'missing AccountSchema'
assert hasattr(mod, 'SessionSchema'), 'missing SessionSchema'
assert hasattr(mod, 'VerificationTokenSchema'), 'missing VerificationTokenSchema'
