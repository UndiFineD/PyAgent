
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_agent_schema_32fe760b9838.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ActionPlan'), 'missing ActionPlan'
assert hasattr(mod, 'ActionPlans'), 'missing ActionPlans'
assert hasattr(mod, 'AgentAndToolsConfig'), 'missing AgentAndToolsConfig'
assert hasattr(mod, 'AgentConfig'), 'missing AgentConfig'
