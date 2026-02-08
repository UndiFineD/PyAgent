
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_cuda_e5b1029b1567.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CUDAAccelerator'), 'missing CUDAAccelerator'
assert hasattr(mod, 'find_usable_cuda_devices'), 'missing find_usable_cuda_devices'
assert hasattr(mod, '_get_all_visible_cuda_devices'), 'missing _get_all_visible_cuda_devices'
assert hasattr(mod, 'num_cuda_devices'), 'missing num_cuda_devices'
assert hasattr(mod, 'is_cuda_available'), 'missing is_cuda_available'
assert hasattr(mod, '_is_ampere_or_later'), 'missing _is_ampere_or_later'
assert hasattr(mod, '_check_cuda_matmul_precision'), 'missing _check_cuda_matmul_precision'
assert hasattr(mod, '_clear_cuda_memory'), 'missing _clear_cuda_memory'
