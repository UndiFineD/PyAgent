
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_visualizer_tool_b2da34ac5839.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'test_visualizer_tool_arun'), 'missing test_visualizer_tool_arun'
