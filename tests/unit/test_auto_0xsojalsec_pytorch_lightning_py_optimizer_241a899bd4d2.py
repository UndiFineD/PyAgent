
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_optimizer_241a899bd4d2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_optimizers_to_device'), 'missing _optimizers_to_device'
assert hasattr(mod, '_optimizer_to_device'), 'missing _optimizer_to_device'
