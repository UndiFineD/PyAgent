
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_test_memory_usage_75e7fa20c739.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_memory_usage'), 'missing get_memory_usage'
assert hasattr(mod, 'mock_onnx_setup'), 'missing mock_onnx_setup'
assert hasattr(mod, 'TestMemoryUsage'), 'missing TestMemoryUsage'
