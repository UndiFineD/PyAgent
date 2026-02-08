
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_sql_tool_f8e67902ac84.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'patch_check_init'), 'missing patch_check_init'
assert hasattr(mod, 'sql_tool_db'), 'missing sql_tool_db'
assert hasattr(mod, 'sql_tool'), 'missing sql_tool'
assert hasattr(mod, 'test_list_tables'), 'missing test_list_tables'
assert hasattr(mod, 'test_sql_query_generation'), 'missing test_sql_query_generation'
assert hasattr(mod, 'test_sql_query_generation_no_tables'), 'missing test_sql_query_generation_no_tables'
assert hasattr(mod, 'test_sql_tool_run'), 'missing test_sql_tool_run'
