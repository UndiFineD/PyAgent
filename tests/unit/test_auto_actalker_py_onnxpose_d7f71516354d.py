
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_onnxpose_d7f71516354d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'preprocess'), 'missing preprocess'
assert hasattr(mod, 'inference'), 'missing inference'
assert hasattr(mod, 'postprocess'), 'missing postprocess'
assert hasattr(mod, 'bbox_xyxy2cs'), 'missing bbox_xyxy2cs'
assert hasattr(mod, '_fix_aspect_ratio'), 'missing _fix_aspect_ratio'
assert hasattr(mod, '_rotate_point'), 'missing _rotate_point'
assert hasattr(mod, '_get_3rd_point'), 'missing _get_3rd_point'
assert hasattr(mod, 'get_warp_matrix'), 'missing get_warp_matrix'
assert hasattr(mod, 'top_down_affine'), 'missing top_down_affine'
assert hasattr(mod, 'get_simcc_maximum'), 'missing get_simcc_maximum'
assert hasattr(mod, 'decode'), 'missing decode'
assert hasattr(mod, 'inference_pose'), 'missing inference_pose'
