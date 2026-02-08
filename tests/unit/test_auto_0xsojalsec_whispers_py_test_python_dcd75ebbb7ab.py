
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whispers_py_test_python_dcd75ebbb7ab.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_pairs'), 'missing test_pairs'
assert hasattr(mod, 'test_is_key'), 'missing test_is_key'
assert hasattr(mod, 'test_is_value'), 'missing test_is_value'
assert hasattr(mod, 'test_traverse_parse'), 'missing test_traverse_parse'
assert hasattr(mod, 'test_traverse_extract'), 'missing test_traverse_extract'
