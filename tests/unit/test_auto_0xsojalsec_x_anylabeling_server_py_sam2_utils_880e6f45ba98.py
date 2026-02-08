
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_sam2_utils_880e6f45ba98.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'select_closest_cond_frames'), 'missing select_closest_cond_frames'
assert hasattr(mod, 'get_1d_sine_pe'), 'missing get_1d_sine_pe'
assert hasattr(mod, 'get_activation_fn'), 'missing get_activation_fn'
assert hasattr(mod, 'get_clones'), 'missing get_clones'
assert hasattr(mod, 'DropPath'), 'missing DropPath'
assert hasattr(mod, 'MLP'), 'missing MLP'
assert hasattr(mod, 'LayerNorm2d'), 'missing LayerNorm2d'
assert hasattr(mod, 'sample_box_points'), 'missing sample_box_points'
assert hasattr(mod, 'sample_random_points_from_errors'), 'missing sample_random_points_from_errors'
assert hasattr(mod, 'sample_one_point_from_error_center'), 'missing sample_one_point_from_error_center'
assert hasattr(mod, 'get_next_point'), 'missing get_next_point'
