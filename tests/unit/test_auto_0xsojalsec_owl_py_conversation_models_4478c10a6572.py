
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_conversation_models_4478c10a6572.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ShareGPTMessage'), 'missing ShareGPTMessage'
assert hasattr(mod, 'ShareGPTConversation'), 'missing ShareGPTConversation'
assert hasattr(mod, 'ToolCall'), 'missing ToolCall'
assert hasattr(mod, 'ToolResponse'), 'missing ToolResponse'
