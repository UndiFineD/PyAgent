
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_deprecated_b7d63deec716.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FadeInFromDown'), 'missing FadeInFromDown'
assert hasattr(mod, 'FadeOutAndShiftDown'), 'missing FadeOutAndShiftDown'
assert hasattr(mod, 'FadeInFromLarge'), 'missing FadeInFromLarge'
