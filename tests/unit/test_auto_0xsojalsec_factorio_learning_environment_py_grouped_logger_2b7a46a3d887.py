
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_grouped_logger_2b7a46a3d887.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'InstanceGroupMetrics'), 'missing InstanceGroupMetrics'
assert hasattr(mod, 'InstanceMetrics'), 'missing InstanceMetrics'
assert hasattr(mod, 'GroupedFactorioLogger'), 'missing GroupedFactorioLogger'
