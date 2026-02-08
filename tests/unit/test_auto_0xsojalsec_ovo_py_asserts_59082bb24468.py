
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_asserts_59082bb24468.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'assert_equal'), 'missing assert_equal'
assert hasattr(mod, 'assert_not_equal'), 'missing assert_not_equal'
assert hasattr(mod, 'assert_true'), 'missing assert_true'
assert hasattr(mod, 'assert_false'), 'missing assert_false'
assert hasattr(mod, 'assert_element_exists'), 'missing assert_element_exists'
assert hasattr(mod, 'assert_no_error_on_page'), 'missing assert_no_error_on_page'
assert hasattr(mod, 'assert_no_error_on_exception'), 'missing assert_no_error_on_exception'
