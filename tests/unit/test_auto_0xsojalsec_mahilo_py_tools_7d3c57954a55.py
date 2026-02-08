
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mahilo_py_tools_7d3c57954a55.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_chat_with_agent_tool_pydanticai'), 'missing get_chat_with_agent_tool_pydanticai'
assert hasattr(mod, 'chat_with_agent_tool_pydanticai'), 'missing chat_with_agent_tool_pydanticai'
