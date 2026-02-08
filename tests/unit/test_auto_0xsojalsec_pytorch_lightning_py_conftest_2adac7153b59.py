
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_conftest_2adac7153b59.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'reset_deterministic_algorithm'), 'missing reset_deterministic_algorithm'
assert hasattr(mod, 'reset_cudnn_benchmark'), 'missing reset_cudnn_benchmark'
