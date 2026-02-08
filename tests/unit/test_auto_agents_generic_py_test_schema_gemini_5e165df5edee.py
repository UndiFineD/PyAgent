
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_schema_gemini_5e165df5edee.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_json_def_replaced'), 'missing test_json_def_replaced'
assert hasattr(mod, 'test_json_def_replaced_any_of'), 'missing test_json_def_replaced_any_of'
assert hasattr(mod, 'test_json_def_recursive'), 'missing test_json_def_recursive'
assert hasattr(mod, 'test_json_def_date'), 'missing test_json_def_date'
