
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_cluster_bdc7f2a12a83.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ClusterType'), 'missing ClusterType'
assert hasattr(mod, '_guess_cluster_type'), 'missing _guess_cluster_type'
assert hasattr(mod, 'get_cluster_type'), 'missing get_cluster_type'
assert hasattr(mod, 'get_checkpoint_path'), 'missing get_checkpoint_path'
assert hasattr(mod, 'get_user_checkpoint_path'), 'missing get_user_checkpoint_path'
assert hasattr(mod, 'get_slurm_partition'), 'missing get_slurm_partition'
assert hasattr(mod, 'get_slurm_executor_parameters'), 'missing get_slurm_executor_parameters'
