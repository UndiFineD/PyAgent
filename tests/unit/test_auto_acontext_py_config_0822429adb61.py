
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_config_0822429adb61.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomScoringRule'), 'missing CustomScoringRule'
assert hasattr(mod, 'ProjectConfig'), 'missing ProjectConfig'
assert hasattr(mod, 'CoreConfig'), 'missing CoreConfig'
assert hasattr(mod, 'filter_value_from_env'), 'missing filter_value_from_env'
assert hasattr(mod, 'filter_value_from_yaml'), 'missing filter_value_from_yaml'
assert hasattr(mod, 'filter_value_from_json'), 'missing filter_value_from_json'
assert hasattr(mod, 'post_validate_core_config_sanity'), 'missing post_validate_core_config_sanity'
