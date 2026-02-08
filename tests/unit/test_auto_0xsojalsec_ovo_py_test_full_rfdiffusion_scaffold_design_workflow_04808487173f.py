
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_full_rfdiffusion_scaffold_design_workflow_04808487173f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_scaffold_end_to_end_logic'), 'missing test_scaffold_end_to_end_logic'
