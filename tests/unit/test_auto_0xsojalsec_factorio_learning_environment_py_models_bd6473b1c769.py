
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_models_bd6473b1c769.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FactorioServer'), 'missing FactorioServer'
assert hasattr(mod, 'Recipe'), 'missing Recipe'
assert hasattr(mod, 'ResourcePatch'), 'missing ResourcePatch'
