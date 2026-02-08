
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_basic_2d0f0c0ccafa.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'load_images_as_tensor'), 'missing load_images_as_tensor'
assert hasattr(mod, 'tensor_to_pil'), 'missing tensor_to_pil'
assert hasattr(mod, 'array_to_pil'), 'missing array_to_pil'
assert hasattr(mod, 'rotate_target_dim_to_last_axis'), 'missing rotate_target_dim_to_last_axis'
assert hasattr(mod, 'preprocess_tensor_for_pi3'), 'missing preprocess_tensor_for_pi3'
assert hasattr(mod, 'write_ply'), 'missing write_ply'
