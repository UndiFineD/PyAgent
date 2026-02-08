
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_base_747b77a8fd5e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MemoryBlock'), 'missing MemoryBlock'
assert hasattr(mod, 'BaseContextCreator'), 'missing BaseContextCreator'
assert hasattr(mod, 'AgentMemory'), 'missing AgentMemory'
