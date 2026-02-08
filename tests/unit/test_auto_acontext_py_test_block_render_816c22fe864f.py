
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_test_block_render_816c22fe864f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TestRenderSOPBlock'), 'missing TestRenderSOPBlock'
assert hasattr(mod, 'TestRenderTextBlock'), 'missing TestRenderTextBlock'
assert hasattr(mod, 'TestRenderContentBlock'), 'missing TestRenderContentBlock'
