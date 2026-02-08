
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_engine_f38b1da8d2af.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AttrDict'), 'missing AttrDict'
assert hasattr(mod, 'staticproperty'), 'missing staticproperty'
assert hasattr(mod, 'World'), 'missing World'
assert hasattr(mod, 'Textures'), 'missing Textures'
assert hasattr(mod, 'GlobalView'), 'missing GlobalView'
assert hasattr(mod, 'UncoverView'), 'missing UncoverView'
assert hasattr(mod, 'LocalView'), 'missing LocalView'
assert hasattr(mod, 'ItemView'), 'missing ItemView'
assert hasattr(mod, 'SemanticView'), 'missing SemanticView'
assert hasattr(mod, '_inside'), 'missing _inside'
assert hasattr(mod, '_draw'), 'missing _draw'
assert hasattr(mod, '_draw_alpha'), 'missing _draw_alpha'
