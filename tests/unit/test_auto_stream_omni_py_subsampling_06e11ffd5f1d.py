
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_subsampling_06e11ffd5f1d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BaseSubsampling'), 'missing BaseSubsampling'
assert hasattr(mod, 'EmbedinigNoSubsampling'), 'missing EmbedinigNoSubsampling'
assert hasattr(mod, 'LinearNoSubsampling'), 'missing LinearNoSubsampling'
assert hasattr(mod, 'Conv1dSubsampling2'), 'missing Conv1dSubsampling2'
assert hasattr(mod, 'Conv2dSubsampling4'), 'missing Conv2dSubsampling4'
assert hasattr(mod, 'Conv2dSubsampling6'), 'missing Conv2dSubsampling6'
assert hasattr(mod, 'Conv2dSubsampling8'), 'missing Conv2dSubsampling8'
assert hasattr(mod, 'LegacyLinearNoSubsampling'), 'missing LegacyLinearNoSubsampling'
