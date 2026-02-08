
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_utilities_8daa729ad627.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_version'), 'missing _version'
assert hasattr(mod, '_scan_checkpoints'), 'missing _scan_checkpoints'
assert hasattr(mod, '_log_hyperparams'), 'missing _log_hyperparams'
