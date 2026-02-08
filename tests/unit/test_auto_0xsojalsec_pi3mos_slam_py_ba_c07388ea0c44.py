
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_ba_c07388ea0c44.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CholeskySolver'), 'missing CholeskySolver'
assert hasattr(mod, 'safe_scatter_add_mat'), 'missing safe_scatter_add_mat'
assert hasattr(mod, 'safe_scatter_add_vec'), 'missing safe_scatter_add_vec'
assert hasattr(mod, 'disp_retr'), 'missing disp_retr'
assert hasattr(mod, 'pose_retr'), 'missing pose_retr'
assert hasattr(mod, 'block_matmul'), 'missing block_matmul'
assert hasattr(mod, 'block_solve'), 'missing block_solve'
assert hasattr(mod, 'block_show'), 'missing block_show'
assert hasattr(mod, 'BA'), 'missing BA'
