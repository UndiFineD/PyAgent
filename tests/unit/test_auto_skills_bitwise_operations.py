
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\skills_bitwise_operations.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'unsigned_left_shift'), 'missing unsigned_left_shift'
assert hasattr(mod, 'unsigned_right_shift'), 'missing unsigned_right_shift'
