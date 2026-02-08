
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_analysis_utils_08998ccb50e9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'group_results_by_model'), 'missing group_results_by_model'
assert hasattr(mod, 'group_results_by_task'), 'missing group_results_by_task'
assert hasattr(mod, 'calculate_pass_at_k'), 'missing calculate_pass_at_k'
assert hasattr(mod, 'get_trajectory_summary'), 'missing get_trajectory_summary'
assert hasattr(mod, 'extract_task_metadata'), 'missing extract_task_metadata'
assert hasattr(mod, 'calculate_efficiency_metrics'), 'missing calculate_efficiency_metrics'
assert hasattr(mod, 'find_performance_outliers'), 'missing find_performance_outliers'
assert hasattr(mod, 'aggregate_results_by_time'), 'missing aggregate_results_by_time'
assert hasattr(mod, 'compare_model_performance_statistical'), 'missing compare_model_performance_statistical'
assert hasattr(mod, 'create_leaderboard'), 'missing create_leaderboard'
