
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_xpander_py_async_function_caller_140060a3e28f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'execute_local_functions'), 'missing execute_local_functions'
assert hasattr(mod, '_execute_single_function'), 'missing _execute_single_function'
