
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_kubeflow_61e0a1e550eb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_default_attributes'), 'missing test_default_attributes'
assert hasattr(mod, 'test_attributes_from_environment_variables'), 'missing test_attributes_from_environment_variables'
assert hasattr(mod, 'test_detect_kubeflow'), 'missing test_detect_kubeflow'
