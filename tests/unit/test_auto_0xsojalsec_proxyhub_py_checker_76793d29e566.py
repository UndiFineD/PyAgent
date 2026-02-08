
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_proxyhub_py_checker_76793d29e566.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Checker'), 'missing Checker'
assert hasattr(mod, '_request'), 'missing _request'
assert hasattr(mod, '_send_test_request'), 'missing _send_test_request'
assert hasattr(mod, '_decompress_content'), 'missing _decompress_content'
assert hasattr(mod, '_check_test_response'), 'missing _check_test_response'
assert hasattr(mod, '_get_anonymity_lvl'), 'missing _get_anonymity_lvl'
assert hasattr(mod, 'ProxyChecker'), 'missing ProxyChecker'
