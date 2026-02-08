
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_registry_863463faa0d4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_AcceleratorRegistry'), 'missing _AcceleratorRegistry'
assert hasattr(mod, 'call_register_accelerators'), 'missing call_register_accelerators'
