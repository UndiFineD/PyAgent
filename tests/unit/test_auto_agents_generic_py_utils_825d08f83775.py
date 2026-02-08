
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_utils_825d08f83775.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'replace_words'), 'missing replace_words'
assert hasattr(mod, 'replace_words'), 'missing replace_words'
assert hasattr(mod, 'replace_words'), 'missing replace_words'
