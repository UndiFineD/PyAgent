
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\action_py_accounts_74c2e11ff325.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Account'), 'missing Account'
assert hasattr(mod, 'get_share_price'), 'missing get_share_price'
