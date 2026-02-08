
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videorag_py_split_3c88954c700d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'split_video'), 'missing split_video'
assert hasattr(mod, 'saving_video_segments'), 'missing saving_video_segments'
