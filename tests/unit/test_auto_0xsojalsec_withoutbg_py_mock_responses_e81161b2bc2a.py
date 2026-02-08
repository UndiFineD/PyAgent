
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_mock_responses_e81161b2bc2a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_mock_api_responses'), 'missing get_mock_api_responses'
assert hasattr(mod, 'create_mock_response'), 'missing create_mock_response'
