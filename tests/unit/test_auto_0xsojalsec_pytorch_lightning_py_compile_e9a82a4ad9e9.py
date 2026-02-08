
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_compile_e9a82a4ad9e9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'from_compiled'), 'missing from_compiled'
assert hasattr(mod, 'to_uncompiled'), 'missing to_uncompiled'
assert hasattr(mod, '_maybe_unwrap_optimized'), 'missing _maybe_unwrap_optimized'
assert hasattr(mod, '_verify_strategy_supports_compile'), 'missing _verify_strategy_supports_compile'
