
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_cached_db_6fbee0a28162.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_cached_project_ids_and_names'), 'missing get_cached_project_ids_and_names'
assert hasattr(mod, 'get_cached_available_descriptors'), 'missing get_cached_available_descriptors'
assert hasattr(mod, 'get_cached_descriptor_values'), 'missing get_cached_descriptor_values'
assert hasattr(mod, 'get_cached_design'), 'missing get_cached_design'
assert hasattr(mod, 'get_cached_designs'), 'missing get_cached_designs'
assert hasattr(mod, 'get_cached_design_ids'), 'missing get_cached_design_ids'
assert hasattr(mod, 'get_cached_round'), 'missing get_cached_round'
assert hasattr(mod, 'get_cached_rounds'), 'missing get_cached_rounds'
assert hasattr(mod, 'get_cached_pool'), 'missing get_cached_pool'
assert hasattr(mod, 'get_cached_pools'), 'missing get_cached_pools'
assert hasattr(mod, 'get_cached_design_jobs'), 'missing get_cached_design_jobs'
assert hasattr(mod, 'get_cached_design_job'), 'missing get_cached_design_job'
assert hasattr(mod, 'get_cached_design_jobs_table'), 'missing get_cached_design_jobs_table'
assert hasattr(mod, '_get_cached_design_jobs_table'), 'missing _get_cached_design_jobs_table'
assert hasattr(mod, 'get_cached_pools_table'), 'missing get_cached_pools_table'
assert hasattr(mod, 'get_cached_design_descriptors'), 'missing get_cached_design_descriptors'
assert hasattr(mod, 'get_cached_designs_accept_field'), 'missing get_cached_designs_accept_field'
assert hasattr(mod, 'get_cached_workflow_pools_and_jobs'), 'missing get_cached_workflow_pools_and_jobs'
