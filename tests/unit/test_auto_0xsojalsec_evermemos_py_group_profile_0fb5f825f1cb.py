
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_group_profile_0fb5f825f1cb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TopicInfo'), 'missing TopicInfo'
assert hasattr(mod, 'RoleUser'), 'missing RoleUser'
assert hasattr(mod, 'RoleAssignment'), 'missing RoleAssignment'
assert hasattr(mod, 'GroupProfile'), 'missing GroupProfile'
