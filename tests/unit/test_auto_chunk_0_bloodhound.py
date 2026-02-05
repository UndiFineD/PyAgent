
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_bloodhound.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'add_user_bh'), 'missing add_user_bh'
assert hasattr(mod, '_add_with_domain'), 'missing _add_with_domain'
assert hasattr(mod, '_add_without_domain'), 'missing _add_without_domain'
