
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_grover_d7e12f3253df.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GroverPreview'), 'missing GroverPreview'
assert hasattr(mod, 'ClassicalSearch'), 'missing ClassicalSearch'
