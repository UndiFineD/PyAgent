
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_segment_anything_2_99df7514249c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LRUCache'), 'missing LRUCache'
assert hasattr(mod, 'SegmentAnything2'), 'missing SegmentAnything2'
