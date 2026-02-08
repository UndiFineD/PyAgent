
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_memory_encoder_d331bc6a1ab3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MaskDownSampler'), 'missing MaskDownSampler'
assert hasattr(mod, 'CXBlock'), 'missing CXBlock'
assert hasattr(mod, 'Fuser'), 'missing Fuser'
assert hasattr(mod, 'MemoryEncoder'), 'missing MemoryEncoder'
