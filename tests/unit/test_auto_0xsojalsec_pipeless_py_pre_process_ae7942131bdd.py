
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pipeless_py_pre_process_ae7942131bdd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'is_cuda_available'), 'missing is_cuda_available'
assert hasattr(mod, 'resize_and_pad'), 'missing resize_and_pad'
assert hasattr(mod, 'resize_with_padding'), 'missing resize_with_padding'
assert hasattr(mod, 'hook'), 'missing hook'
