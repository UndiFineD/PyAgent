
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_submission_components_28010275d6d8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pool_submission_inputs'), 'missing pool_submission_inputs'
assert hasattr(mod, 'get_pool_inputs'), 'missing get_pool_inputs'
assert hasattr(mod, 'review_workflow_submission'), 'missing review_workflow_submission'
assert hasattr(mod, 'submit_workflow_dialog'), 'missing submit_workflow_dialog'
assert hasattr(mod, 'create_new_round_dialog'), 'missing create_new_round_dialog'
assert hasattr(mod, 'show_rfdiffusion_binder_seq_design_inputs'), 'missing show_rfdiffusion_binder_seq_design_inputs'
assert hasattr(mod, 'show_rfdiffusion_advanced_settings'), 'missing show_rfdiffusion_advanced_settings'
assert hasattr(mod, 'customize_json_settings_component'), 'missing customize_json_settings_component'
assert hasattr(mod, 'show_bindcraft_advanced_settings'), 'missing show_bindcraft_advanced_settings'
