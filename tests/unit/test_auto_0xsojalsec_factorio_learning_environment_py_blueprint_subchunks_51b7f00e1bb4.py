
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_blueprint_subchunks_51b7f00e1bb4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SubchunkConfig'), 'missing SubchunkConfig'
assert hasattr(mod, 'get_entities_in_region'), 'missing get_entities_in_region'
assert hasattr(mod, 'extract_subchunk'), 'missing extract_subchunk'
assert hasattr(mod, 'generate_subchunks'), 'missing generate_subchunks'
assert hasattr(mod, 'create_subchunk_augmented_dataset'), 'missing create_subchunk_augmented_dataset'
assert hasattr(mod, 'create_overlapping_subchunks'), 'missing create_overlapping_subchunks'
assert hasattr(mod, 'create_adaptive_subchunks'), 'missing create_adaptive_subchunks'
