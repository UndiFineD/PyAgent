
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_utils_3b2686453a14.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'is_state_dict_equal'), 'missing is_state_dict_equal'
assert hasattr(mod, 'is_timing_close'), 'missing is_timing_close'
assert hasattr(mod, 'is_cuda_memory_close'), 'missing is_cuda_memory_close'
assert hasattr(mod, 'make_deterministic'), 'missing make_deterministic'
assert hasattr(mod, 'get_model_input_dtype'), 'missing get_model_input_dtype'
assert hasattr(mod, 'cuda_reset'), 'missing cuda_reset'
