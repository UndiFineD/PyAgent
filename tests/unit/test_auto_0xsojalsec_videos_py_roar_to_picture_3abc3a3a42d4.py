
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_roar_to_picture_3abc3a3a42d4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DecomposeRoar_SlowFPS'), 'missing DecomposeRoar_SlowFPS'
assert hasattr(mod, 'CombineWavesToImage_SlowFPS'), 'missing CombineWavesToImage_SlowFPS'
