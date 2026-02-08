
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_design_logic_rfdiffusion_cfd41e7136ea.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'submit_rfdiffusion_preview'), 'missing submit_rfdiffusion_preview'
assert hasattr(mod, 'process_workflow_results'), 'missing process_workflow_results'
assert hasattr(mod, 'process_rfdiffusion_design'), 'missing process_rfdiffusion_design'
assert hasattr(mod, 'prepare_rfdiffusion_workflow_params'), 'missing prepare_rfdiffusion_workflow_params'
assert hasattr(mod, 'get_rfdiffusion_run_parameters'), 'missing get_rfdiffusion_run_parameters'
