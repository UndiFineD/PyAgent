
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_modified_resnet_dd94c9c21276.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Bottleneck'), 'missing Bottleneck'
assert hasattr(mod, 'AttentionPool2d'), 'missing AttentionPool2d'
assert hasattr(mod, 'ModifiedResNet'), 'missing ModifiedResNet'
