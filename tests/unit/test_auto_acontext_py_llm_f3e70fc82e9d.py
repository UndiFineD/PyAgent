
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_llm_f3e70fc82e9d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FunctionSchema'), 'missing FunctionSchema'
assert hasattr(mod, 'ToolSchema'), 'missing ToolSchema'
assert hasattr(mod, 'LLMFunction'), 'missing LLMFunction'
assert hasattr(mod, 'LLMToolCall'), 'missing LLMToolCall'
assert hasattr(mod, 'LLMResponse'), 'missing LLMResponse'
