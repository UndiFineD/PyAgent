
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_agent_abc_a693f19176a0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AgentABC'), 'missing AgentABC'
assert hasattr(mod, 'create_default_agent_card'), 'missing create_default_agent_card'
