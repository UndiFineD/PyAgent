
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_agent_util_ad8bdb4c34f5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'assemble_memory_input'), 'missing assemble_memory_input'
assert hasattr(mod, 'assemble_memory_output'), 'missing assemble_memory_output'
assert hasattr(mod, 'process_agent_llm_config'), 'missing process_agent_llm_config'
