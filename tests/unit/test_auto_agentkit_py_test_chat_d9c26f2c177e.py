
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_chat_d9c26f2c177e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'chat_query'), 'missing chat_query'
assert hasattr(mod, 'test_chat'), 'missing test_chat'
