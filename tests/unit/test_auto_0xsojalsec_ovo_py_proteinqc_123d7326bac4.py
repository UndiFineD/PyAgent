
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_proteinqc_123d7326bac4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'proteinqc_fragment'), 'missing proteinqc_fragment'
assert hasattr(mod, 'submit_proteinqc_dialog'), 'missing submit_proteinqc_dialog'
