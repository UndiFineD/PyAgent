
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_chat_aef90f0b1d3c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'init_chat'), 'missing init_chat'
assert hasattr(mod, 'add_response'), 'missing add_response'
assert hasattr(mod, 'add_multiimage_response'), 'missing add_multiimage_response'
assert hasattr(mod, 'print_status'), 'missing print_status'
