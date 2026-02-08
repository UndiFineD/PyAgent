
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_chat_ctx_4ee1997688b6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ai_function1'), 'missing ai_function1'
assert hasattr(mod, 'test_args_model'), 'missing test_args_model'
assert hasattr(mod, 'test_dict'), 'missing test_dict'
