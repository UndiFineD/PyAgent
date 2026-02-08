
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_worldgen_a5d276c1870f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_world'), 'missing generate_world'
assert hasattr(mod, '_set_material'), 'missing _set_material'
assert hasattr(mod, '_set_object'), 'missing _set_object'
assert hasattr(mod, '_simplex'), 'missing _simplex'
