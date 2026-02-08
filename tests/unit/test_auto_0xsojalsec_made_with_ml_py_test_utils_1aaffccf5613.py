
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_test_utils_1aaffccf5613.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_set_seed'), 'missing test_set_seed'
assert hasattr(mod, 'test_save_and_load_dict'), 'missing test_save_and_load_dict'
assert hasattr(mod, 'test_pad_array'), 'missing test_pad_array'
assert hasattr(mod, 'test_collate_fn'), 'missing test_collate_fn'
assert hasattr(mod, 'test_dict_to_list'), 'missing test_dict_to_list'
