
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_prettymapp_py_test_osm_7af58a591c6b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_get_osm_tags'), 'missing test_get_osm_tags'
assert hasattr(mod, 'test_get_osm_geometries_from_xml'), 'missing test_get_osm_geometries_from_xml'
