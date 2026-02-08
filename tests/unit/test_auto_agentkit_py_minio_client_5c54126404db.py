
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_minio_client_5c54126404db.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'IMinioResponse'), 'missing IMinioResponse'
assert hasattr(mod, 'MinioClient'), 'missing MinioClient'
