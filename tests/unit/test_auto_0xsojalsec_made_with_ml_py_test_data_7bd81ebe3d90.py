
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_test_data_7bd81ebe3d90.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'df'), 'missing df'
assert hasattr(mod, 'class_to_index'), 'missing class_to_index'
assert hasattr(mod, 'test_load_data'), 'missing test_load_data'
assert hasattr(mod, 'test_stratify_split'), 'missing test_stratify_split'
assert hasattr(mod, 'test_clean_text'), 'missing test_clean_text'
assert hasattr(mod, 'test_preprocess'), 'missing test_preprocess'
assert hasattr(mod, 'test_fit_transform'), 'missing test_fit_transform'
