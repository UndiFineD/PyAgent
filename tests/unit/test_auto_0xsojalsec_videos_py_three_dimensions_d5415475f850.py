
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_three_dimensions_d5415475f850.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'OldStars'), 'missing OldStars'
assert hasattr(mod, 'OldCubeWithFaces'), 'missing OldCubeWithFaces'
assert hasattr(mod, 'OldCube'), 'missing OldCube'
assert hasattr(mod, 'OldOctohedron'), 'missing OldOctohedron'
assert hasattr(mod, 'OldDodecahedron'), 'missing OldDodecahedron'
assert hasattr(mod, 'OldSphere'), 'missing OldSphere'
