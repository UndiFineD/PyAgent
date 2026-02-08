
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mantis_py_notifications_302626995b82.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Notifications'), 'missing Notifications'
assert hasattr(mod, 'NotificationsUtils'), 'missing NotificationsUtils'
