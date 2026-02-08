
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_design_logic_e75ce345b282.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_design_jobs_table'), 'missing get_design_jobs_table'
assert hasattr(mod, 'get_pools_table'), 'missing get_pools_table'
assert hasattr(mod, 'format_pool_status'), 'missing format_pool_status'
assert hasattr(mod, 'get_workflows_table'), 'missing get_workflows_table'
assert hasattr(mod, 'submit_design_workflow'), 'missing submit_design_workflow'
assert hasattr(mod, 'get_log'), 'missing get_log'
assert hasattr(mod, 'process_results'), 'missing process_results'
assert hasattr(mod, 'update_acceptance_thresholds'), 'missing update_acceptance_thresholds'
assert hasattr(mod, 'update_accepted_design_ids'), 'missing update_accepted_design_ids'
assert hasattr(mod, 'set_designs_accepted'), 'missing set_designs_accepted'
assert hasattr(mod, 'collect_storage_paths'), 'missing collect_storage_paths'
