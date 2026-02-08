
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\ace_plus_py_ace_plus_dataset_04c1c3aace2a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'load_image'), 'missing load_image'
assert hasattr(mod, 'transform_image'), 'missing transform_image'
assert hasattr(mod, 'transform_mask'), 'missing transform_mask'
assert hasattr(mod, 'ensure_src_align_target_h_mode'), 'missing ensure_src_align_target_h_mode'
assert hasattr(mod, 'ensure_src_align_target_padding_mode'), 'missing ensure_src_align_target_padding_mode'
assert hasattr(mod, 'ensure_limit_sequence'), 'missing ensure_limit_sequence'
assert hasattr(mod, 'ACEPlusDataset'), 'missing ACEPlusDataset'
