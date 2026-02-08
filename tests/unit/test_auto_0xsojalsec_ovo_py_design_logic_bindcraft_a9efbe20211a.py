
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_design_logic_bindcraft_a9efbe20211a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'prepare_bindcraft_params'), 'missing prepare_bindcraft_params'
assert hasattr(mod, 'process_workflow_results'), 'missing process_workflow_results'
