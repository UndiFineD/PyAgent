
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_resolver_9f623b75979b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ConnectionPoint'), 'missing ConnectionPoint'
assert hasattr(mod, 'ConnectionType'), 'missing ConnectionType'
assert hasattr(mod, 'PositionResolver'), 'missing PositionResolver'
assert hasattr(mod, 'Resolver'), 'missing Resolver'
