
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_full_rfdiffusion_fastrelax_binder_design_workflow_3c1589ed56b9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_binder_default_end_to_end_logic'), 'missing test_binder_default_end_to_end_logic'
