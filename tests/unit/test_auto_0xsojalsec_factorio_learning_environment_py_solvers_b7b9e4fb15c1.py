
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_solvers_b7b9e4fb15c1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_blueprint_title_and_purpose'), 'missing generate_blueprint_title_and_purpose'
assert hasattr(mod, 'entity_removal_denoising'), 'missing entity_removal_denoising'
assert hasattr(mod, 'validate_denoising_qa'), 'missing validate_denoising_qa'
assert hasattr(mod, 'generate_spatial_context_question'), 'missing generate_spatial_context_question'
