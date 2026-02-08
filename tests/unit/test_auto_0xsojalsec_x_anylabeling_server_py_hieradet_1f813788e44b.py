
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_hieradet_1f813788e44b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'do_pool'), 'missing do_pool'
assert hasattr(mod, 'MultiScaleAttention'), 'missing MultiScaleAttention'
assert hasattr(mod, 'MultiScaleBlock'), 'missing MultiScaleBlock'
assert hasattr(mod, 'Hiera'), 'missing Hiera'
