
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_praisonai_py_autoagents_e12c64ef8f9c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TaskConfig'), 'missing TaskConfig'
assert hasattr(mod, 'AgentConfig'), 'missing AgentConfig'
assert hasattr(mod, 'AutoAgentsConfig'), 'missing AutoAgentsConfig'
assert hasattr(mod, 'AutoAgents'), 'missing AutoAgents'
