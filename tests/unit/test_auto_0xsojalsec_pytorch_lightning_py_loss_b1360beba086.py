
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_loss_b1360beba086.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'policy_loss'), 'missing policy_loss'
assert hasattr(mod, 'value_loss'), 'missing value_loss'
assert hasattr(mod, 'entropy_loss'), 'missing entropy_loss'
