
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_sockets_ae9a0ce44ca0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SocketEvents'), 'missing SocketEvents'
assert hasattr(mod, 'MessageType'), 'missing MessageType'
assert hasattr(mod, 'MessageDisplayType'), 'missing MessageDisplayType'
assert hasattr(mod, 'Message'), 'missing Message'
assert hasattr(mod, 'SocketMessage'), 'missing SocketMessage'
