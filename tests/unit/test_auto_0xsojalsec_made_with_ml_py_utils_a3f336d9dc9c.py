
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_utils_a3f336d9dc9c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_experiment_name'), 'missing generate_experiment_name'
assert hasattr(mod, 'delete_experiment'), 'missing delete_experiment'
