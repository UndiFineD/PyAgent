
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_optim_utils_76600eac53dd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'make_pypose_Sim3'), 'missing make_pypose_Sim3'
assert hasattr(mod, 'SE3_to_Sim3'), 'missing SE3_to_Sim3'
assert hasattr(mod, '_format'), 'missing _format'
assert hasattr(mod, 'reduce_edges'), 'missing reduce_edges'
assert hasattr(mod, 'umeyama_alignment'), 'missing umeyama_alignment'
assert hasattr(mod, 'ransac_umeyama'), 'missing ransac_umeyama'
assert hasattr(mod, 'batch_jacobian'), 'missing batch_jacobian'
assert hasattr(mod, '_residual'), 'missing _residual'
assert hasattr(mod, 'residual'), 'missing residual'
assert hasattr(mod, 'run_DPVO_PGO'), 'missing run_DPVO_PGO'
assert hasattr(mod, 'perform_updates'), 'missing perform_updates'
