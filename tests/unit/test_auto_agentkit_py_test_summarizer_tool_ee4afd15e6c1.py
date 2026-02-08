
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_summarizer_tool_ee4afd15e6c1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'summarizer_tool_input'), 'missing summarizer_tool_input'
assert hasattr(mod, 'summarizer_tool'), 'missing summarizer_tool'
assert hasattr(mod, 'test_summarizer_tool_run_short_input'), 'missing test_summarizer_tool_run_short_input'
assert hasattr(mod, 'test_summarizer_tool_run_long_input'), 'missing test_summarizer_tool_run_long_input'
