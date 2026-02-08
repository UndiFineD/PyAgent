
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_mps_23af66929cd5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MPSAccelerator'), 'missing MPSAccelerator'
assert hasattr(mod, '_get_all_available_mps_gpus'), 'missing _get_all_available_mps_gpus'
