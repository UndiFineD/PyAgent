
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_proxyhub_py_test_negotiators_ecab7bbe2791.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'proxy'), 'missing proxy'
assert hasattr(mod, 'test_base_attrs'), 'missing test_base_attrs'
assert hasattr(mod, 'test_socks_negotiate'), 'missing test_socks_negotiate'
assert hasattr(mod, 'test_socks_negotiate_error'), 'missing test_socks_negotiate_error'
assert hasattr(mod, 'test_connect_negotiate'), 'missing test_connect_negotiate'
assert hasattr(mod, 'test_connect_negotiate_error'), 'missing test_connect_negotiate_error'
