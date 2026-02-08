
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_uploads_129bf88d38f4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FileUpload'), 'missing FileUpload'
assert hasattr(mod, 'normalize_file_upload'), 'missing normalize_file_upload'
