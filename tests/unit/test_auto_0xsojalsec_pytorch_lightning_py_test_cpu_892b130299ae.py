
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_cpu_892b130299ae.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_auto_device_count'), 'missing test_auto_device_count'
assert hasattr(mod, 'test_availability'), 'missing test_availability'
assert hasattr(mod, 'test_init_device_with_wrong_device_type'), 'missing test_init_device_with_wrong_device_type'
assert hasattr(mod, 'test_get_parallel_devices'), 'missing test_get_parallel_devices'
assert hasattr(mod, 'test_invalid_devices_with_cpu_accelerator'), 'missing test_invalid_devices_with_cpu_accelerator'
