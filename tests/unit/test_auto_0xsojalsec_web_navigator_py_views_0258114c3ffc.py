
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_web_navigator_py_views_0258114c3ffc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DOMHistoryElementNode'), 'missing DOMHistoryElementNode'
assert hasattr(mod, 'HashElement'), 'missing HashElement'
