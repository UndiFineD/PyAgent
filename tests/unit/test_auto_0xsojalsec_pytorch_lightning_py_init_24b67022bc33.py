
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_init_24b67022bc33.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_EmptyInit'), 'missing _EmptyInit'
assert hasattr(mod, '_materialize'), 'missing _materialize'
assert hasattr(mod, '_materialize_meta_tensors'), 'missing _materialize_meta_tensors'
assert hasattr(mod, '_materialize_distributed_module'), 'missing _materialize_distributed_module'
assert hasattr(mod, '_has_meta_device_parameters_or_buffers'), 'missing _has_meta_device_parameters_or_buffers'
