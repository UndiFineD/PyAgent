
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_colors_eafa04b65480.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_color_from_str'), 'missing get_color_from_str'
assert hasattr(mod, 'darken_lighten'), 'missing darken_lighten'
assert hasattr(mod, 'lighten'), 'missing lighten'
assert hasattr(mod, 'darken'), 'missing darken'
