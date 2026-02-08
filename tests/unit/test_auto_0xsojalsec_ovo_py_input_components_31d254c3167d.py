
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_input_components_31d254c3167d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'initialize_workflow'), 'missing initialize_workflow'
assert hasattr(mod, 'pdb_input_component'), 'missing pdb_input_component'
assert hasattr(mod, 'sequence_selection_fragment'), 'missing sequence_selection_fragment'
