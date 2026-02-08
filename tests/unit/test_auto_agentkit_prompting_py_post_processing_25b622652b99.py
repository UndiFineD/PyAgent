
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_post_processing_25b622652b99.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SubgoalAfterQuery'), 'missing SubgoalAfterQuery'
assert hasattr(mod, 'SkillAfterQuery'), 'missing SkillAfterQuery'
assert hasattr(mod, 'AdaptiveAfterQuery'), 'missing AdaptiveAfterQuery'
assert hasattr(mod, 'KBAddAfterQuery'), 'missing KBAddAfterQuery'
assert hasattr(mod, 'KBReasonAfterQuery'), 'missing KBReasonAfterQuery'
assert hasattr(mod, 'ReflectionAfterQuery'), 'missing ReflectionAfterQuery'
assert hasattr(mod, 'ListActionAfterQuery'), 'missing ListActionAfterQuery'
assert hasattr(mod, 'ActionSummaryAfterQuery'), 'missing ActionSummaryAfterQuery'
assert hasattr(mod, 'ActionAfterQuery'), 'missing ActionAfterQuery'
assert hasattr(mod, 'SummaryAfterQuery'), 'missing SummaryAfterQuery'
