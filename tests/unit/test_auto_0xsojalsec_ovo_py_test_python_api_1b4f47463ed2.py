
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_python_api_1b4f47463ed2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_create_project'), 'missing test_create_project'
assert hasattr(mod, 'test_schedule_valid_params'), 'missing test_schedule_valid_params'
assert hasattr(mod, 'test_schedule_invalid_params'), 'missing test_schedule_invalid_params'
assert hasattr(mod, 'test_design_id'), 'missing test_design_id'
