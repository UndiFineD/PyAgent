
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_auto_regression_85e1e77c9b54.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_gpt2_tokenizer'), 'missing get_gpt2_tokenizer'
assert hasattr(mod, 'get_gpt2_model'), 'missing get_gpt2_model'
assert hasattr(mod, 'gpt2_predict_next_token'), 'missing gpt2_predict_next_token'
assert hasattr(mod, 'gpt3_predict_next_token'), 'missing gpt3_predict_next_token'
assert hasattr(mod, 'SimpleAutogregression'), 'missing SimpleAutogregression'
assert hasattr(mod, 'AnnotateNextWord'), 'missing AnnotateNextWord'
assert hasattr(mod, 'QuickerRegression'), 'missing QuickerRegression'
assert hasattr(mod, 'AutoregressionGPT3'), 'missing AutoregressionGPT3'
assert hasattr(mod, 'QuickRegressionGPT3'), 'missing QuickRegressionGPT3'
assert hasattr(mod, 'GPT3CleverestAutocomplete'), 'missing GPT3CleverestAutocomplete'
assert hasattr(mod, 'GPT3OnLearningSimpler'), 'missing GPT3OnLearningSimpler'
assert hasattr(mod, 'ModelTakingInTextWithSurroundingPieces'), 'missing ModelTakingInTextWithSurroundingPieces'
assert hasattr(mod, 'AthleteCompletion'), 'missing AthleteCompletion'
assert hasattr(mod, 'ThatWhichDoesNotKillMe'), 'missing ThatWhichDoesNotKillMe'
