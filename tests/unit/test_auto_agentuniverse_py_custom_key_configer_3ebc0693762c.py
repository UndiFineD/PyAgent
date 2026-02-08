
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_custom_key_configer_3ebc0693762c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomKeyConfiger'), 'missing CustomKeyConfiger'
