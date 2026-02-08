
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_handler_15cbef2b6551.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'A2AMessage'), 'missing A2AMessage'
assert hasattr(mod, 'A2AProtocolHandler'), 'missing A2AProtocolHandler'
