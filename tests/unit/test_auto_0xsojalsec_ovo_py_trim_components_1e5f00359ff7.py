
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_trim_components_1e5f00359ff7.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'parameters_trim_structure_component'), 'missing parameters_trim_structure_component'
assert hasattr(mod, 'trimmed_structure_visualizer'), 'missing trimmed_structure_visualizer'
assert hasattr(mod, 'check_hotspots'), 'missing check_hotspots'
