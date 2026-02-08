
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_groupable_entities_f5843e58e39e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_deduplicate_entities'), 'missing _deduplicate_entities'
assert hasattr(mod, '_construct_group'), 'missing _construct_group'
assert hasattr(mod, 'consolidate_underground_belts'), 'missing consolidate_underground_belts'
assert hasattr(mod, 'construct_belt_groups'), 'missing construct_belt_groups'
assert hasattr(mod, 'agglomerate_groupable_entities'), 'missing agglomerate_groupable_entities'
