
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_counting_d5a39271d5c6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CountingScene'), 'missing CountingScene'
assert hasattr(mod, 'PowerCounter'), 'missing PowerCounter'
assert hasattr(mod, 'CountInDecimal'), 'missing CountInDecimal'
assert hasattr(mod, 'CountInTernary'), 'missing CountInTernary'
assert hasattr(mod, 'CountInBinaryTo256'), 'missing CountInBinaryTo256'
assert hasattr(mod, 'FactorialBase'), 'missing FactorialBase'
