
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_amp_230669ae051a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MixedPrecision'), 'missing MixedPrecision'
assert hasattr(mod, '_optimizer_handles_unscaling'), 'missing _optimizer_handles_unscaling'
