
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_colorpp.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'color'), 'missing color'
assert hasattr(mod, 'pretty_convert'), 'missing pretty_convert'
assert hasattr(mod, 'walk_obj'), 'missing walk_obj'
assert hasattr(mod, 'pprint'), 'missing pprint'
assert hasattr(mod, 'pprintf'), 'missing pprintf'
