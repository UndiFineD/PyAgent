
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_plot_utils_309816c534d8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'plot_trajectory'), 'missing plot_trajectory'
assert hasattr(mod, 'save_output_for_COLMAP'), 'missing save_output_for_COLMAP'
assert hasattr(mod, 'save_ply'), 'missing save_ply'
