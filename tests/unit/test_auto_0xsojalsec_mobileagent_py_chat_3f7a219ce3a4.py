
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_chat_3f7a219ce3a4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'init_action_chat'), 'missing init_action_chat'
assert hasattr(mod, 'init_reflect_chat'), 'missing init_reflect_chat'
assert hasattr(mod, 'init_memory_chat'), 'missing init_memory_chat'
assert hasattr(mod, 'add_response_old'), 'missing add_response_old'
assert hasattr(mod, 'add_response'), 'missing add_response'
assert hasattr(mod, 'add_response_two_image'), 'missing add_response_two_image'
assert hasattr(mod, 'print_status'), 'missing print_status'
