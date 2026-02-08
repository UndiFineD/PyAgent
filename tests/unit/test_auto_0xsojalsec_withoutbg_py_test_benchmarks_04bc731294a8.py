
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_test_benchmarks_04bc731294a8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'benchmark_images'), 'missing benchmark_images'
assert hasattr(mod, 'mock_onnx_setup'), 'missing mock_onnx_setup'
assert hasattr(mod, 'TestProcessingBenchmarks'), 'missing TestProcessingBenchmarks'
assert hasattr(mod, 'TestScalabilityBenchmarks'), 'missing TestScalabilityBenchmarks'
assert hasattr(mod, 'TestRegressionBenchmarks'), 'missing TestRegressionBenchmarks'
