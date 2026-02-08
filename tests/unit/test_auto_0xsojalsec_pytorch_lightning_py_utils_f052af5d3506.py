
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_utils_f052af5d3506.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_convert_fp_tensor'), 'missing _convert_fp_tensor'
assert hasattr(mod, '_DtypeContextManager'), 'missing _DtypeContextManager'
assert hasattr(mod, '_ClassReplacementContextManager'), 'missing _ClassReplacementContextManager'
