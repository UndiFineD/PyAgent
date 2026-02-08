
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_make_circuit_boards_py_kicad6_datamodel_99986f48449d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'KicadField'), 'missing KicadField'
assert hasattr(mod, 'KicadPin'), 'missing KicadPin'
assert hasattr(mod, 'KicadLibpart'), 'missing KicadLibpart'
assert hasattr(mod, 'KicadSheetpath'), 'missing KicadSheetpath'
assert hasattr(mod, 'KicadComponent'), 'missing KicadComponent'
assert hasattr(mod, 'KicadNode'), 'missing KicadNode'
assert hasattr(mod, 'KicadNet'), 'missing KicadNet'
assert hasattr(mod, 'KicadLibraries'), 'missing KicadLibraries'
assert hasattr(mod, 'KicadNetlist'), 'missing KicadNetlist'
