
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whispers_py_test_secrets_357f309fb8e9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_exclude_by_keys_and_values'), 'missing test_exclude_by_keys_and_values'
assert hasattr(mod, 'test_detection_by_key'), 'missing test_detection_by_key'
assert hasattr(mod, 'test_detection_by_value'), 'missing test_detection_by_value'
assert hasattr(mod, 'test_detection_by_filename'), 'missing test_detection_by_filename'
assert hasattr(mod, 'test_detection_by_rule'), 'missing test_detection_by_rule'
assert hasattr(mod, 'test_is_static'), 'missing test_is_static'
