
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_mvcr_b506a324f1c6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'HoldUpMultivariableChainRule'), 'missing HoldUpMultivariableChainRule'
assert hasattr(mod, 'ComputationalNetwork'), 'missing ComputationalNetwork'
