
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_box_utils_0adff6f76c83.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'nms_'), 'missing nms_'
assert hasattr(mod, 'decode'), 'missing decode'
assert hasattr(mod, 'nms'), 'missing nms'
assert hasattr(mod, 'Detect'), 'missing Detect'
assert hasattr(mod, 'PriorBox'), 'missing PriorBox'
