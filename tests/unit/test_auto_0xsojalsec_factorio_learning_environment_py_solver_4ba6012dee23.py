
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_solver_4ba6012dee23.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_action_sequence'), 'missing generate_action_sequence'
assert hasattr(mod, 'generate_next_action_questions'), 'missing generate_next_action_questions'
assert hasattr(mod, 'generate_construction_order_questions'), 'missing generate_construction_order_questions'
