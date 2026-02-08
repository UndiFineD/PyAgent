
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_messages_610085b03dd6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MessagePart'), 'missing MessagePart'
assert hasattr(mod, 'AcontextMessage'), 'missing AcontextMessage'
assert hasattr(mod, 'build_acontext_message'), 'missing build_acontext_message'
assert hasattr(mod, 'normalize_message_part'), 'missing normalize_message_part'
