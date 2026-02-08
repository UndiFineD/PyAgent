
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_hooks_0cbfc682a2f6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ModelHooks'), 'missing ModelHooks'
assert hasattr(mod, 'DataHooks'), 'missing DataHooks'
assert hasattr(mod, 'CheckpointHooks'), 'missing CheckpointHooks'
