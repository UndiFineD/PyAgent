
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_enum_de39d3e42de3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MemoryTypeEnum'), 'missing MemoryTypeEnum'
assert hasattr(mod, 'ChatMessageEnum'), 'missing ChatMessageEnum'
