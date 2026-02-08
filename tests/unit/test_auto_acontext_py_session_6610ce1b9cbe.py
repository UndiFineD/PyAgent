
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_session_6610ce1b9cbe.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Asset'), 'missing Asset'
assert hasattr(mod, 'Part'), 'missing Part'
assert hasattr(mod, 'Message'), 'missing Message'
assert hasattr(mod, 'Session'), 'missing Session'
assert hasattr(mod, 'Task'), 'missing Task'
assert hasattr(mod, 'ListSessionsOutput'), 'missing ListSessionsOutput'
assert hasattr(mod, 'PublicURL'), 'missing PublicURL'
assert hasattr(mod, 'GetMessagesOutput'), 'missing GetMessagesOutput'
assert hasattr(mod, 'GetTasksOutput'), 'missing GetTasksOutput'
assert hasattr(mod, 'LearningStatus'), 'missing LearningStatus'
assert hasattr(mod, 'TokenCounts'), 'missing TokenCounts'
