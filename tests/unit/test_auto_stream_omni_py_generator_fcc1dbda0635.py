
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_generator_fcc1dbda0635.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ResBlock'), 'missing ResBlock'
assert hasattr(mod, 'SineGen'), 'missing SineGen'
assert hasattr(mod, 'SourceModuleHnNSF'), 'missing SourceModuleHnNSF'
assert hasattr(mod, 'HiFTGenerator'), 'missing HiFTGenerator'
