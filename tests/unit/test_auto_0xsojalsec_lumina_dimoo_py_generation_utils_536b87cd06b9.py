
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_lumina_dimoo_py_generation_utils_536b87cd06b9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'add_gumbel_noise'), 'missing add_gumbel_noise'
assert hasattr(mod, 'cosine_schedule'), 'missing cosine_schedule'
assert hasattr(mod, 'gumbel_noise'), 'missing gumbel_noise'
assert hasattr(mod, 'gumbel_max_sample'), 'missing gumbel_max_sample'
assert hasattr(mod, 'mask_by_random_topk'), 'missing mask_by_random_topk'
assert hasattr(mod, 'get_num_transfer_tokens'), 'missing get_num_transfer_tokens'
assert hasattr(mod, 'setup_seed'), 'missing setup_seed'
