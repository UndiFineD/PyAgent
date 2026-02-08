
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_sop_block_a71b685a196e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SOPStep'), 'missing SOPStep'
assert hasattr(mod, 'SOPData'), 'missing SOPData'
assert hasattr(mod, 'SubmitSOPData'), 'missing SubmitSOPData'
assert hasattr(mod, 'SOPBlock'), 'missing SOPBlock'
