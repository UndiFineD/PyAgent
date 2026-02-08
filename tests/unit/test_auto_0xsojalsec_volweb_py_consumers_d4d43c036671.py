
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_consumers_d4d43c036671.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'VolatilityTaskConsumer'), 'missing VolatilityTaskConsumer'
assert hasattr(mod, 'CasesTaskConsumer'), 'missing CasesTaskConsumer'
assert hasattr(mod, 'EvidencesTaskConsumer'), 'missing EvidencesTaskConsumer'
assert hasattr(mod, 'SymbolsTaskConsumer'), 'missing SymbolsTaskConsumer'
