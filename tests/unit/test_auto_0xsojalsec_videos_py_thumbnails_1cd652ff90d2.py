
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_thumbnails_1cd652ff90d2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Chapter0'), 'missing Chapter0'
assert hasattr(mod, 'Chapter1'), 'missing Chapter1'
assert hasattr(mod, 'Chapter2'), 'missing Chapter2'
assert hasattr(mod, 'Chapter3'), 'missing Chapter3'
assert hasattr(mod, 'Chapter4p1'), 'missing Chapter4p1'
assert hasattr(mod, 'Chapter4p2'), 'missing Chapter4p2'
assert hasattr(mod, 'Chapter5'), 'missing Chapter5'
assert hasattr(mod, 'Chapter9'), 'missing Chapter9'
assert hasattr(mod, 'Chapter10'), 'missing Chapter10'
