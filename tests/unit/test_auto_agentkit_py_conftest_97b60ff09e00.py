
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_conftest_97b60ff09e00.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pytest_configure'), 'missing pytest_configure'
assert hasattr(mod, 'mock_redis_client_sync'), 'missing mock_redis_client_sync'
assert hasattr(mod, 'messages'), 'missing messages'
assert hasattr(mod, 'llm'), 'missing llm'
assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'tool_input'), 'missing tool_input'
assert hasattr(mod, 'agent_config'), 'missing agent_config'
assert hasattr(mod, 'meta_agent'), 'missing meta_agent'
assert hasattr(mod, 'test_client'), 'missing test_client'
assert hasattr(mod, 'run_manager'), 'missing run_manager'
