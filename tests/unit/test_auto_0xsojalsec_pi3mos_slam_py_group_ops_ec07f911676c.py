
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_group_ops_ec07f911676c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GroupOp'), 'missing GroupOp'
assert hasattr(mod, 'Exp'), 'missing Exp'
assert hasattr(mod, 'Log'), 'missing Log'
assert hasattr(mod, 'Inv'), 'missing Inv'
assert hasattr(mod, 'Mul'), 'missing Mul'
assert hasattr(mod, 'Adj'), 'missing Adj'
assert hasattr(mod, 'AdjT'), 'missing AdjT'
assert hasattr(mod, 'Act3'), 'missing Act3'
assert hasattr(mod, 'Act4'), 'missing Act4'
assert hasattr(mod, 'Jinv'), 'missing Jinv'
assert hasattr(mod, 'ToMatrix'), 'missing ToMatrix'
assert hasattr(mod, 'FromVec'), 'missing FromVec'
assert hasattr(mod, 'ToVec'), 'missing ToVec'
