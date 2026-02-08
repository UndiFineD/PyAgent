
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\adfspoof_py_utils_30ac0675b208.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'random_string'), 'missing random_string'
assert hasattr(mod, 'new_guid'), 'missing new_guid'
assert hasattr(mod, 'encode_object_guid'), 'missing encode_object_guid'
assert hasattr(mod, 'die'), 'missing die'
assert hasattr(mod, 'print_intro'), 'missing print_intro'
