
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_transform_article_449455c3c54d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'half_plane'), 'missing half_plane'
assert hasattr(mod, 'SingleVariableFunction'), 'missing SingleVariableFunction'
assert hasattr(mod, 'LineToPlaneFunction'), 'missing LineToPlaneFunction'
assert hasattr(mod, 'PlaneToPlaneFunctionSeparatePlanes'), 'missing PlaneToPlaneFunctionSeparatePlanes'
assert hasattr(mod, 'PlaneToPlaneFunction'), 'missing PlaneToPlaneFunction'
assert hasattr(mod, 'PlaneToLineFunction'), 'missing PlaneToLineFunction'
assert hasattr(mod, 'PlaneToSpaceFunction'), 'missing PlaneToSpaceFunction'
assert hasattr(mod, 'SpaceToSpaceFunction'), 'missing SpaceToSpaceFunction'
