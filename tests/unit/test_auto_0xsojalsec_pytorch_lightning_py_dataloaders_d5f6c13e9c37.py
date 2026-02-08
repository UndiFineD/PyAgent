
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_dataloaders_d5f6c13e9c37.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomInfDataloader'), 'missing CustomInfDataloader'
assert hasattr(mod, 'CustomNotImplementedErrorDataloader'), 'missing CustomNotImplementedErrorDataloader'
