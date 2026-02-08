
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi0_lerobot_py_visualize_dataset_rerun_7186167b6b45.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ViewDatasetArgs'), 'missing ViewDatasetArgs'
assert hasattr(mod, 'EpisodeSampler'), 'missing EpisodeSampler'
assert hasattr(mod, 'to_hwc_uint8_numpy'), 'missing to_hwc_uint8_numpy'
assert hasattr(mod, 'visualize_dataset'), 'missing visualize_dataset'
assert hasattr(mod, 'new_main'), 'missing new_main'
