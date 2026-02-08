
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_single_device_e7073c48e393.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_can_instantiate_without_args'), 'missing test_can_instantiate_without_args'
assert hasattr(mod, 'test_create_group'), 'missing test_create_group'
