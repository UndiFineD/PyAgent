
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_score_based_4b24d6cea91c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_ContextUnit'), 'missing _ContextUnit'
assert hasattr(mod, 'ScoreBasedContextCreator'), 'missing ScoreBasedContextCreator'
