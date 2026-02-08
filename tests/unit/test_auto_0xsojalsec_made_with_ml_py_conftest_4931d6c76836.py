
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_conftest_4931d6c76836.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pytest_addoption'), 'missing pytest_addoption'
assert hasattr(mod, 'run_id'), 'missing run_id'
assert hasattr(mod, 'predictor'), 'missing predictor'
