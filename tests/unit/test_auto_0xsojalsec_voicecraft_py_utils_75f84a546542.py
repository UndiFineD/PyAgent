
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_voicecraft_py_utils_75f84a546542.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'make_pad_mask'), 'missing make_pad_mask'
assert hasattr(mod, 'generate_partial_autoregressive_mask'), 'missing generate_partial_autoregressive_mask'
