
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_dynamic_prog_04617e9ec6f2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_value_grid'), 'missing get_value_grid'
assert hasattr(mod, 'highlight_box'), 'missing highlight_box'
assert hasattr(mod, 'get_box_highlight'), 'missing get_box_highlight'
assert hasattr(mod, 'GreedyAlgorithm'), 'missing GreedyAlgorithm'
assert hasattr(mod, 'RecrusiveExhaustiveSearch'), 'missing RecrusiveExhaustiveSearch'
assert hasattr(mod, 'DynamicProgrammingApproachSearch'), 'missing DynamicProgrammingApproachSearch'
