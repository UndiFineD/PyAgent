
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_made_with_ml_py_data_2702cadb4f6a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'load_data'), 'missing load_data'
assert hasattr(mod, 'stratify_split'), 'missing stratify_split'
assert hasattr(mod, 'clean_text'), 'missing clean_text'
assert hasattr(mod, 'tokenize'), 'missing tokenize'
assert hasattr(mod, 'preprocess'), 'missing preprocess'
assert hasattr(mod, 'CustomPreprocessor'), 'missing CustomPreprocessor'
