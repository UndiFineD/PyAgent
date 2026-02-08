
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_nets_c942c590deba.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'L2Norm'), 'missing L2Norm'
assert hasattr(mod, 'S3FDNet'), 'missing S3FDNet'
