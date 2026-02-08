
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_registry_9b3430db6656.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TestAccelerator'), 'missing TestAccelerator'
assert hasattr(mod, 'test_accelerator_registry_with_new_accelerator'), 'missing test_accelerator_registry_with_new_accelerator'
assert hasattr(mod, 'test_available_accelerators_in_registry'), 'missing test_available_accelerators_in_registry'
assert hasattr(mod, 'test_registry_as_decorator'), 'missing test_registry_as_decorator'
assert hasattr(mod, 'test_registry_as_static_method'), 'missing test_registry_as_static_method'
assert hasattr(mod, 'test_registry_without_parameters'), 'missing test_registry_without_parameters'
