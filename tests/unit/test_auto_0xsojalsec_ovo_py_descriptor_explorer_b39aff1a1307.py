
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_explorer_b39aff1a1307.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'HistogramSettings'), 'missing HistogramSettings'
assert hasattr(mod, 'descriptor_explorer'), 'missing descriptor_explorer'
