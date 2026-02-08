
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_cuda_1b3b1e1e2031.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_auto_device_count'), 'missing test_auto_device_count'
assert hasattr(mod, 'test_gpu_availability'), 'missing test_gpu_availability'
assert hasattr(mod, 'test_init_device_with_wrong_device_type'), 'missing test_init_device_with_wrong_device_type'
assert hasattr(mod, 'test_get_parallel_devices'), 'missing test_get_parallel_devices'
assert hasattr(mod, 'test_set_cuda_device'), 'missing test_set_cuda_device'
assert hasattr(mod, 'test_force_nvml_based_cuda_check'), 'missing test_force_nvml_based_cuda_check'
assert hasattr(mod, 'test_tf32_message'), 'missing test_tf32_message'
assert hasattr(mod, 'test_find_usable_cuda_devices_error_handling'), 'missing test_find_usable_cuda_devices_error_handling'
