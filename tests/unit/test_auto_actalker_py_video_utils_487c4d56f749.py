
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_video_utils_487c4d56f749.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'concat_pil'), 'missing concat_pil'
assert hasattr(mod, 'save_videos_from_pil'), 'missing save_videos_from_pil'
assert hasattr(mod, 'save_videos_grid'), 'missing save_videos_grid'
assert hasattr(mod, 'resize_tensor_frames'), 'missing resize_tensor_frames'
assert hasattr(mod, 'pil_list_to_tensor'), 'missing pil_list_to_tensor'
