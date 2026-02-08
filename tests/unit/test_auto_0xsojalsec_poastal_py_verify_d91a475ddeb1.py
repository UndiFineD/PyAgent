
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_poastal_py_verify_d91a475ddeb1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'deliverable'), 'missing deliverable'
assert hasattr(mod, 'spam'), 'missing spam'
assert hasattr(mod, 'disposable'), 'missing disposable'
