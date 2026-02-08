
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_lumina_dimoo_py_image_utils_53d2ca36ffd5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'decode_vq_to_image'), 'missing decode_vq_to_image'
assert hasattr(mod, 'preprocess_image'), 'missing preprocess_image'
assert hasattr(mod, 'calculate_vq_params'), 'missing calculate_vq_params'
assert hasattr(mod, 'center_crop'), 'missing center_crop'
assert hasattr(mod, 'var_center_crop'), 'missing var_center_crop'
assert hasattr(mod, 'generate_crop_size_list'), 'missing generate_crop_size_list'
assert hasattr(mod, 'add_break_line'), 'missing add_break_line'
assert hasattr(mod, 'encode_img_with_breaks'), 'missing encode_img_with_breaks'
assert hasattr(mod, 'encode_img_with_paint'), 'missing encode_img_with_paint'
