
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_conversation_meta_0c20509451c2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'UserDetailModel'), 'missing UserDetailModel'
assert hasattr(mod, 'ConversationMeta'), 'missing ConversationMeta'
