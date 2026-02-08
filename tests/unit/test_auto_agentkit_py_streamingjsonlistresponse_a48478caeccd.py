
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_streamingjsonlistresponse_a48478caeccd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'async_enumerate'), 'missing async_enumerate'
assert hasattr(mod, 'StreamingJsonListResponse'), 'missing StreamingJsonListResponse'
