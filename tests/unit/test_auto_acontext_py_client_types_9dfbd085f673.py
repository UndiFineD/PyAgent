
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_client_types_9dfbd085f673.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RequesterProtocol'), 'missing RequesterProtocol'
assert hasattr(mod, 'AsyncRequesterProtocol'), 'missing AsyncRequesterProtocol'
