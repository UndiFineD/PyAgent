
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_util_b861b3dd51e6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_obj_from_str'), 'missing get_obj_from_str'
assert hasattr(mod, 'instantiate_from_config'), 'missing instantiate_from_config'
assert hasattr(mod, 'ensure_file_written'), 'missing ensure_file_written'
assert hasattr(mod, 'compute_snr'), 'missing compute_snr'
assert hasattr(mod, 'seed_everything'), 'missing seed_everything'
assert hasattr(mod, 'import_filename'), 'missing import_filename'
assert hasattr(mod, 'delete_additional_ckpt'), 'missing delete_additional_ckpt'
assert hasattr(mod, 'save_videos_from_pil'), 'missing save_videos_from_pil'
assert hasattr(mod, 'save_videos_grid'), 'missing save_videos_grid'
assert hasattr(mod, 'read_frames'), 'missing read_frames'
assert hasattr(mod, 'get_fps'), 'missing get_fps'
assert hasattr(mod, 'numpy_to_video'), 'missing numpy_to_video'
assert hasattr(mod, 'calculate_brightness'), 'missing calculate_brightness'
assert hasattr(mod, 'calculate_contrast'), 'missing calculate_contrast'
assert hasattr(mod, 'attention_map_to_image'), 'missing attention_map_to_image'
assert hasattr(mod, 'all_attention_map_to_image'), 'missing all_attention_map_to_image'
