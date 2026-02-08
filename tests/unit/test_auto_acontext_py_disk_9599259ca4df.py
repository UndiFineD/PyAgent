
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_disk_9599259ca4df.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Disk'), 'missing Disk'
assert hasattr(mod, 'ListDisksOutput'), 'missing ListDisksOutput'
assert hasattr(mod, 'Artifact'), 'missing Artifact'
assert hasattr(mod, 'FileContent'), 'missing FileContent'
assert hasattr(mod, 'GetArtifactResp'), 'missing GetArtifactResp'
assert hasattr(mod, 'ListArtifactsResp'), 'missing ListArtifactsResp'
assert hasattr(mod, 'UpdateArtifactResp'), 'missing UpdateArtifactResp'
