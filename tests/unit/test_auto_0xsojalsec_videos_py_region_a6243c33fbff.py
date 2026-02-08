
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_region_a6243c33fbff.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Region'), 'missing Region'
assert hasattr(mod, 'HalfPlane'), 'missing HalfPlane'
assert hasattr(mod, 'region_from_line_boundary'), 'missing region_from_line_boundary'
assert hasattr(mod, 'region_from_polygon_vertices'), 'missing region_from_polygon_vertices'
assert hasattr(mod, 'plane_partition'), 'missing plane_partition'
assert hasattr(mod, 'plane_partition_from_points'), 'missing plane_partition_from_points'
