
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_langgraph_d1c66b23296e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LLMAdapter'), 'missing LLMAdapter'
assert hasattr(mod, 'LangGraphStream'), 'missing LangGraphStream'
assert hasattr(mod, '_to_chat_chunk'), 'missing _to_chat_chunk'
