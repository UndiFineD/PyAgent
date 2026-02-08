
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_web_navigator_py_views_d67161bbd814.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BoundingBox'), 'missing BoundingBox'
assert hasattr(mod, 'CenterCord'), 'missing CenterCord'
assert hasattr(mod, 'DOMElementNode'), 'missing DOMElementNode'
assert hasattr(mod, 'ScrollElementNode'), 'missing ScrollElementNode'
assert hasattr(mod, 'DOMTextualNode'), 'missing DOMTextualNode'
assert hasattr(mod, 'DOMState'), 'missing DOMState'
