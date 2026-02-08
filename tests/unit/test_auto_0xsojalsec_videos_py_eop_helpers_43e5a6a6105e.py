
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_eop_helpers_43e5a6a6105e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'binary'), 'missing binary'
assert hasattr(mod, 'nb_of_ones'), 'missing nb_of_ones'
assert hasattr(mod, 'rainbow_color'), 'missing rainbow_color'
assert hasattr(mod, 'graded_color'), 'missing graded_color'
