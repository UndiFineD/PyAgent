
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_prompt_796bc04d1224.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_action_prompt'), 'missing get_action_prompt'
assert hasattr(mod, 'get_reflect_prompt'), 'missing get_reflect_prompt'
assert hasattr(mod, 'get_memory_prompt'), 'missing get_memory_prompt'
assert hasattr(mod, 'get_process_prompt'), 'missing get_process_prompt'
