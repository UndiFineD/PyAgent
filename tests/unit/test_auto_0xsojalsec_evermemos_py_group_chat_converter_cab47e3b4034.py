
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_group_chat_converter_cab47e3b4034.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'convert_group_chat_format_to_memorize_input'), 'missing convert_group_chat_format_to_memorize_input'
assert hasattr(mod, '_convert_message_to_internal_format'), 'missing _convert_message_to_internal_format'
assert hasattr(mod, '_parse_datetime_with_timezone'), 'missing _parse_datetime_with_timezone'
assert hasattr(mod, 'convert_simple_message_to_memorize_input'), 'missing convert_simple_message_to_memorize_input'
assert hasattr(mod, 'validate_group_chat_format_input'), 'missing validate_group_chat_format_input'
