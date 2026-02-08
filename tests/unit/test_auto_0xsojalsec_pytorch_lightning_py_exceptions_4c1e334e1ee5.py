
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_exceptions_4c1e334e1ee5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SIGTERMException'), 'missing SIGTERMException'
assert hasattr(mod, '_TunerExitException'), 'missing _TunerExitException'
assert hasattr(mod, '_augment_message'), 'missing _augment_message'
