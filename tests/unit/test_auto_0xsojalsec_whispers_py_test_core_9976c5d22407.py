
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whispers_py_test_core_9976c5d22407.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_run'), 'missing test_run'
assert hasattr(mod, 'test_load_config_exception'), 'missing test_load_config_exception'
assert hasattr(mod, 'test_load_config'), 'missing test_load_config'
assert hasattr(mod, 'test_include_files'), 'missing test_include_files'
assert hasattr(mod, 'test_exclude_files'), 'missing test_exclude_files'
