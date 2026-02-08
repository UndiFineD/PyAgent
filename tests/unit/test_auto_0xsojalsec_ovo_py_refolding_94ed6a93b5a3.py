
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_refolding_94ed6a93b5a3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'refolding_fragment'), 'missing refolding_fragment'
assert hasattr(mod, 'submit_refolding_dialog'), 'missing submit_refolding_dialog'
