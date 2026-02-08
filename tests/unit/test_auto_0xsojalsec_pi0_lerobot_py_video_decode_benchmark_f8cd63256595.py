
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi0_lerobot_py_video_decode_benchmark_f8cd63256595.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BenchmarkConfig'), 'missing BenchmarkConfig'
assert hasattr(mod, 'benchmark_decode'), 'missing benchmark_decode'
