
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_memory_query_91c07dd392c5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FetchMemRequest'), 'missing FetchMemRequest'
assert hasattr(mod, 'FetchMemResponse'), 'missing FetchMemResponse'
assert hasattr(mod, 'RetrieveMemRequest'), 'missing RetrieveMemRequest'
assert hasattr(mod, 'RetrieveMemResponse'), 'missing RetrieveMemResponse'
assert hasattr(mod, 'UserDetail'), 'missing UserDetail'
assert hasattr(mod, 'ConversationMetaRequest'), 'missing ConversationMetaRequest'
