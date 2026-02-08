
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_tpu_e3c7d3776cd2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_graveyard_single_tpu'), 'missing test_graveyard_single_tpu'
assert hasattr(mod, 'test_graveyard_no_device'), 'missing test_graveyard_no_device'
