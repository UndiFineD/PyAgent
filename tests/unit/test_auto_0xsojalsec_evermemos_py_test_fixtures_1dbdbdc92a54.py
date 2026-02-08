
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_test_fixtures_1dbdbdc92a54.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'UserRepository'), 'missing UserRepository'
assert hasattr(mod, 'MySQLUserRepository'), 'missing MySQLUserRepository'
assert hasattr(mod, 'PostgreSQLUserRepository'), 'missing PostgreSQLUserRepository'
assert hasattr(mod, 'MockUserRepository'), 'missing MockUserRepository'
assert hasattr(mod, 'UserService'), 'missing UserService'
assert hasattr(mod, 'UserServiceImpl'), 'missing UserServiceImpl'
assert hasattr(mod, 'NotificationService'), 'missing NotificationService'
assert hasattr(mod, 'EmailNotificationService'), 'missing EmailNotificationService'
assert hasattr(mod, 'SMSNotificationService'), 'missing SMSNotificationService'
assert hasattr(mod, 'PushNotificationService'), 'missing PushNotificationService'
assert hasattr(mod, 'EmailService'), 'missing EmailService'
assert hasattr(mod, 'SMTPEmailService'), 'missing SMTPEmailService'
assert hasattr(mod, 'DatabaseConnection'), 'missing DatabaseConnection'
assert hasattr(mod, 'create_database_connection'), 'missing create_database_connection'
assert hasattr(mod, 'create_readonly_connection'), 'missing create_readonly_connection'
assert hasattr(mod, 'PrototypeService'), 'missing PrototypeService'
assert hasattr(mod, 'CacheService'), 'missing CacheService'
assert hasattr(mod, 'RedisCacheService'), 'missing RedisCacheService'
assert hasattr(mod, 'MemoryCacheService'), 'missing MemoryCacheService'
assert hasattr(mod, 'register_standard_beans'), 'missing register_standard_beans'
