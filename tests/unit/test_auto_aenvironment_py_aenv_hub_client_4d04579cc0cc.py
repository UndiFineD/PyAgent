
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_aenv_hub_client_4d04579cc0cc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EnvStatus'), 'missing EnvStatus'
assert hasattr(mod, 'AEnvHubError'), 'missing AEnvHubError'
assert hasattr(mod, 'AuthenticationError'), 'missing AuthenticationError'
assert hasattr(mod, 'NotFoundError'), 'missing NotFoundError'
assert hasattr(mod, 'ValidationError'), 'missing ValidationError'
assert hasattr(mod, 'RateLimitError'), 'missing RateLimitError'
assert hasattr(mod, 'AEnvHubClient'), 'missing AEnvHubClient'
