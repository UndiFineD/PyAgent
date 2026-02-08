
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_utils_67998aba7e20.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'position_grid_to_embed'), 'missing position_grid_to_embed'
assert hasattr(mod, 'make_sincos_pos_embed'), 'missing make_sincos_pos_embed'
assert hasattr(mod, 'create_uv_grid'), 'missing create_uv_grid'
