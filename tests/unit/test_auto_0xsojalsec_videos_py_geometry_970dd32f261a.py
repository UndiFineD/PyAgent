
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_geometry_970dd32f261a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FakeAreaManipulation'), 'missing FakeAreaManipulation'
assert hasattr(mod, 'LogarithmicSpiral'), 'missing LogarithmicSpiral'
