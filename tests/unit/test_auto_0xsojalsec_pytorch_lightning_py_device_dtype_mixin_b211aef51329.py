
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_device_dtype_mixin_b211aef51329.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_DeviceDtypeModuleMixin'), 'missing _DeviceDtypeModuleMixin'
assert hasattr(mod, '_update_properties'), 'missing _update_properties'
