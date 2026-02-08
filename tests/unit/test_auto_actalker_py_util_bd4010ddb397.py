
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_util_bd4010ddb397.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'seed_everything'), 'missing seed_everything'
assert hasattr(mod, 'import_filename'), 'missing import_filename'
assert hasattr(mod, 'delete_additional_ckpt'), 'missing delete_additional_ckpt'
assert hasattr(mod, 'save_videos_from_pil'), 'missing save_videos_from_pil'
assert hasattr(mod, 'save_videos_grid'), 'missing save_videos_grid'
assert hasattr(mod, 'read_frames'), 'missing read_frames'
assert hasattr(mod, 'get_fps'), 'missing get_fps'
