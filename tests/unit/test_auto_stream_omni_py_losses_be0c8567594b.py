
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_losses_be0c8567594b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'tpr_loss'), 'missing tpr_loss'
assert hasattr(mod, 'mel_loss'), 'missing mel_loss'
