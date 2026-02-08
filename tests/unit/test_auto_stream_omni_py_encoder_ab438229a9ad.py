
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_encoder_ab438229a9ad.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BaseEncoder'), 'missing BaseEncoder'
assert hasattr(mod, 'TransformerEncoder'), 'missing TransformerEncoder'
assert hasattr(mod, 'ConformerEncoder'), 'missing ConformerEncoder'
