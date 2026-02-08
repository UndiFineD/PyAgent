
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videorag_py_feature_eb6a926eb1b0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'encode_video_segments'), 'missing encode_video_segments'
assert hasattr(mod, 'encode_string_query'), 'missing encode_string_query'
