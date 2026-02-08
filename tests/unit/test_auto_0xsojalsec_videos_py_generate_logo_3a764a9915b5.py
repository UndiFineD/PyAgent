
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_generate_logo_3a764a9915b5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'drag_pixels'), 'missing drag_pixels'
assert hasattr(mod, 'LogoGeneration'), 'missing LogoGeneration'
