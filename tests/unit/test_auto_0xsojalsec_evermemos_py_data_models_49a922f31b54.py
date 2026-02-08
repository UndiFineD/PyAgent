
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_data_models_49a922f31b54.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Message'), 'missing Message'
assert hasattr(mod, 'Conversation'), 'missing Conversation'
assert hasattr(mod, 'QAPair'), 'missing QAPair'
assert hasattr(mod, 'Dataset'), 'missing Dataset'
assert hasattr(mod, 'SearchResult'), 'missing SearchResult'
assert hasattr(mod, 'AnswerResult'), 'missing AnswerResult'
assert hasattr(mod, 'EvaluationResult'), 'missing EvaluationResult'
