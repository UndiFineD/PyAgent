
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_openai_sdk_0536159d2038.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'convert_openai_tool_to_llm_tool'), 'missing convert_openai_tool_to_llm_tool'
assert hasattr(mod, 'openai_complete'), 'missing openai_complete'
