
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_pytorch_i3d_e91a5b8a649e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MaxPool3dSamePadding'), 'missing MaxPool3dSamePadding'
assert hasattr(mod, 'Unit3D'), 'missing Unit3D'
assert hasattr(mod, 'InceptionModule'), 'missing InceptionModule'
assert hasattr(mod, 'InceptionI3d'), 'missing InceptionI3d'
