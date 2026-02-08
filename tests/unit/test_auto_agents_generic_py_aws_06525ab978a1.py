
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_aws_06525ab978a1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BedrockFormatData'), 'missing BedrockFormatData'
assert hasattr(mod, 'to_chat_ctx'), 'missing to_chat_ctx'
assert hasattr(mod, '_build_image'), 'missing _build_image'
