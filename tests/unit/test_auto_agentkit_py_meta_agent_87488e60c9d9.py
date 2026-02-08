
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_meta_agent_87488e60c9d9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_conv_token_buffer_memory'), 'missing get_conv_token_buffer_memory'
assert hasattr(mod, 'create_meta_agent'), 'missing create_meta_agent'
