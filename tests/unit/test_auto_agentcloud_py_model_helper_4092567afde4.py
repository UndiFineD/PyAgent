
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_model_helper_4092567afde4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_models_attribute_values'), 'missing get_models_attribute_values'
assert hasattr(mod, 'convert_dictionaries_to_models'), 'missing convert_dictionaries_to_models'
assert hasattr(mod, 'keyset'), 'missing keyset'
assert hasattr(mod, 'in_enums'), 'missing in_enums'
assert hasattr(mod, 'get_enum_key_from_value'), 'missing get_enum_key_from_value'
assert hasattr(mod, 'get_enum_value_from_str_key'), 'missing get_enum_value_from_str_key'
assert hasattr(mod, 'match_key'), 'missing match_key'
assert hasattr(mod, 'search_subordinate_keys'), 'missing search_subordinate_keys'
