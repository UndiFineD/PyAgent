
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_m4c_evaluator_81a175a24325.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EvalAIAnswerProcessor'), 'missing EvalAIAnswerProcessor'
assert hasattr(mod, 'TextVQAAccuracyEvaluator'), 'missing TextVQAAccuracyEvaluator'
assert hasattr(mod, 'STVQAAccuracyEvaluator'), 'missing STVQAAccuracyEvaluator'
assert hasattr(mod, 'STVQAANLSEvaluator'), 'missing STVQAANLSEvaluator'
assert hasattr(mod, 'TextCapsBleu4Evaluator'), 'missing TextCapsBleu4Evaluator'
