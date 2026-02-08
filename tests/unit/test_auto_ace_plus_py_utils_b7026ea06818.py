
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\ace_plus_py_utils_b7026ea06818.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'edit_preprocess'), 'missing edit_preprocess'
assert hasattr(mod, 'ACEPlusImageProcessor'), 'missing ACEPlusImageProcessor'
