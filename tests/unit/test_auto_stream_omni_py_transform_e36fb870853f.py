
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_transform_e36fb870853f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ResizeMaxSize'), 'missing ResizeMaxSize'
assert hasattr(mod, '_convert_to_rgb'), 'missing _convert_to_rgb'
assert hasattr(mod, 'image_transform'), 'missing image_transform'
