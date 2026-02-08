
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_hermes_function_formatter_eb10644ac109.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'HermesToolResponse'), 'missing HermesToolResponse'
assert hasattr(mod, 'HermesToolCall'), 'missing HermesToolCall'
assert hasattr(mod, 'HermesFunctionFormatter'), 'missing HermesFunctionFormatter'
