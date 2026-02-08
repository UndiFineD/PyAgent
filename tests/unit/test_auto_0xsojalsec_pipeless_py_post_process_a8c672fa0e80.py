
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pipeless_py_post_process_a8c672fa0e80.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'hook'), 'missing hook'
assert hasattr(mod, 'play_sound'), 'missing play_sound'
assert hasattr(mod, 'draw_piano'), 'missing draw_piano'
assert hasattr(mod, 'is_point_outside_circle'), 'missing is_point_outside_circle'
