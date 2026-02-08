
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_logic_d2a950ea08d7.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_available_descriptors'), 'missing get_available_descriptors'
assert hasattr(mod, 'get_wide_descriptor_table'), 'missing get_wide_descriptor_table'
assert hasattr(mod, 'submit_descriptor_workflow'), 'missing submit_descriptor_workflow'
assert hasattr(mod, 'prepare_proteinqc_params'), 'missing prepare_proteinqc_params'
assert hasattr(mod, 'prepare_refolding_params'), 'missing prepare_refolding_params'
assert hasattr(mod, 'get_log'), 'missing get_log'
assert hasattr(mod, 'process_results'), 'missing process_results'
assert hasattr(mod, 'read_descriptor_file_values'), 'missing read_descriptor_file_values'
assert hasattr(mod, 'save_descriptor_job_for_design_job'), 'missing save_descriptor_job_for_design_job'
assert hasattr(mod, 'find_id_column'), 'missing find_id_column'
assert hasattr(mod, 'generate_descriptor_values_for_design'), 'missing generate_descriptor_values_for_design'
assert hasattr(mod, 'update_and_process_descriptors'), 'missing update_and_process_descriptors'
assert hasattr(mod, 'export_proteinqc_excel'), 'missing export_proteinqc_excel'
assert hasattr(mod, 'export_design_descriptors_excel'), 'missing export_design_descriptors_excel'
