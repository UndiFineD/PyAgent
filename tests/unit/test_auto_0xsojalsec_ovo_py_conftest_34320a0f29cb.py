
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_conftest_34320a0f29cb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'check_unit_test_mode'), 'missing check_unit_test_mode'
assert hasattr(mod, 'project_data'), 'missing project_data'
