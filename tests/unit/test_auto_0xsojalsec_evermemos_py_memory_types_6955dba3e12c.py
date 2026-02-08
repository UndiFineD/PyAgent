
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_memory_types_6955dba3e12c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RawDataType'), 'missing RawDataType'
assert hasattr(mod, 'MemCell'), 'missing MemCell'
assert hasattr(mod, 'BaseMemory'), 'missing BaseMemory'
assert hasattr(mod, 'EpisodeMemory'), 'missing EpisodeMemory'
assert hasattr(mod, 'EventLog'), 'missing EventLog'
assert hasattr(mod, 'Foresight'), 'missing Foresight'
