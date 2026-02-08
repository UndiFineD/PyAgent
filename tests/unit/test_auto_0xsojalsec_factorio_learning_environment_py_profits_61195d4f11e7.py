
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_profits_61195d4f11e7.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'eval_program_with_profits'), 'missing eval_program_with_profits'
assert hasattr(mod, 'get_profits'), 'missing get_profits'
assert hasattr(mod, 'get_new_production_flows'), 'missing get_new_production_flows'
assert hasattr(mod, 'get_static_profits'), 'missing get_static_profits'
assert hasattr(mod, 'get_dynamic_profits'), 'missing get_dynamic_profits'
assert hasattr(mod, 'eval_program_with_achievements'), 'missing eval_program_with_achievements'
assert hasattr(mod, 'get_achievements'), 'missing get_achievements'
assert hasattr(mod, 'get_updated_static_items'), 'missing get_updated_static_items'
assert hasattr(mod, 'process_achievements'), 'missing process_achievements'
