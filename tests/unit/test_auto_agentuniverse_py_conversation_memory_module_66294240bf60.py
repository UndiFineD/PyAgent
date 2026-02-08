
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_conversation_memory_module_66294240bf60.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_relation_str'), 'missing generate_relation_str'
assert hasattr(mod, 'generate_relation_str_en'), 'missing generate_relation_str_en'
assert hasattr(mod, 'sync_to_sub_agent_memory'), 'missing sync_to_sub_agent_memory'
assert hasattr(mod, 'ConversationMemoryModule'), 'missing ConversationMemoryModule'
