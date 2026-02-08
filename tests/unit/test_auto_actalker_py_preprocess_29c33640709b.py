
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_preprocess_29c33640709b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_video_pose'), 'missing get_video_pose'
assert hasattr(mod, 'get_image_pose'), 'missing get_image_pose'
