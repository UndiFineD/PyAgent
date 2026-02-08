
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_cohere_f092045d8c61.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomAsyncClient'), 'missing CustomAsyncClient'
assert hasattr(mod, 'CustomChatCohere'), 'missing CustomChatCohere'
