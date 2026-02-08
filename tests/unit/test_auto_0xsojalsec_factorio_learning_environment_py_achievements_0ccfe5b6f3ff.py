
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_achievements_0ccfe5b6f3ff.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'calculate_achievements'), 'missing calculate_achievements'
assert hasattr(mod, 'eval_program_with_achievements'), 'missing eval_program_with_achievements'
