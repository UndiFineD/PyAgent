
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_test_batch_performance_70b6fed0ae20.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_test_images'), 'missing create_test_images'
assert hasattr(mod, 'mock_processing'), 'missing mock_processing'
assert hasattr(mod, 'TestBatchPerformance'), 'missing TestBatchPerformance'
