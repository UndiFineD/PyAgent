
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_anthropic_sdk_e6dc9fa156a6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'convert_openai_tool_to_anthropic_tool'), 'missing convert_openai_tool_to_anthropic_tool'
assert hasattr(mod, 'process_messages'), 'missing process_messages'
assert hasattr(mod, 'anthropic_complete'), 'missing anthropic_complete'
