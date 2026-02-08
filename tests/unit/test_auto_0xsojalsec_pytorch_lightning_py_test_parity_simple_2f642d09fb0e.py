
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_parity_simple_2f642d09fb0e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'train_torch'), 'missing train_torch'
assert hasattr(mod, 'train_fabric'), 'missing train_fabric'
assert hasattr(mod, 'test_parity_single_device'), 'missing test_parity_single_device'
