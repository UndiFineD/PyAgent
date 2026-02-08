
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_basellm_tool_30ee59230a42.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'basellm_tool'), 'missing basellm_tool'
assert hasattr(mod, 'test_basellm_tool_run'), 'missing test_basellm_tool_run'
