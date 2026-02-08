
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_groups_bb67e1cbbe95.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LieGroupParameter'), 'missing LieGroupParameter'
assert hasattr(mod, 'LieGroup'), 'missing LieGroup'
assert hasattr(mod, 'SO3'), 'missing SO3'
assert hasattr(mod, 'RxSO3'), 'missing RxSO3'
assert hasattr(mod, 'SE3'), 'missing SE3'
assert hasattr(mod, 'Sim3'), 'missing Sim3'
assert hasattr(mod, 'cat'), 'missing cat'
assert hasattr(mod, 'stack'), 'missing stack'
