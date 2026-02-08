
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_model_6b737aacbea8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'sequence_mask'), 'missing sequence_mask'
assert hasattr(mod, 'fix_len_compatibility'), 'missing fix_len_compatibility'
assert hasattr(mod, 'convert_pad_shape'), 'missing convert_pad_shape'
assert hasattr(mod, 'generate_path'), 'missing generate_path'
assert hasattr(mod, 'duration_loss'), 'missing duration_loss'
assert hasattr(mod, 'normalize'), 'missing normalize'
assert hasattr(mod, 'denormalize'), 'missing denormalize'
