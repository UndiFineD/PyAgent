
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_test_behavioral_3ff088fc36c5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_invariance'), 'missing test_invariance'
assert hasattr(mod, 'test_directional'), 'missing test_directional'
assert hasattr(mod, 'test_mft'), 'missing test_mft'
