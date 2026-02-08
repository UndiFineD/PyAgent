
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_agentuniverse_service_pb2_grpc_0fbc882deb3f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AgentUniverseServiceStub'), 'missing AgentUniverseServiceStub'
assert hasattr(mod, 'AgentUniverseServiceServicer'), 'missing AgentUniverseServiceServicer'
assert hasattr(mod, 'add_AgentUniverseServiceServicer_to_server'), 'missing add_AgentUniverseServiceServicer_to_server'
assert hasattr(mod, 'AgentUniverseService'), 'missing AgentUniverseService'
