
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_connection_pool_ba37e57063af.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DummyConnection'), 'missing DummyConnection'
assert hasattr(mod, 'dummy_connect_factory'), 'missing dummy_connect_factory'
assert hasattr(mod, 'test_get_reuses_connection'), 'missing test_get_reuses_connection'
assert hasattr(mod, 'test_get_creates_new_connection_when_none_available'), 'missing test_get_creates_new_connection_when_none_available'
assert hasattr(mod, 'test_remove_connection'), 'missing test_remove_connection'
assert hasattr(mod, 'test_get_expired'), 'missing test_get_expired'
