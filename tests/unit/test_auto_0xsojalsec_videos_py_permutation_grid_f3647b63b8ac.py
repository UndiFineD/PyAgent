
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_permutation_grid_f3647b63b8ac.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'print_permutation'), 'missing print_permutation'
assert hasattr(mod, 'PermutationGrid'), 'missing PermutationGrid'
