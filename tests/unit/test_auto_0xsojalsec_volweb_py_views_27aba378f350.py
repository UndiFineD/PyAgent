
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_views_27aba378f350.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'evidences'), 'missing evidences'
assert hasattr(mod, 'CaseEvidenceApiView'), 'missing CaseEvidenceApiView'
assert hasattr(mod, 'EvidenceAPIView'), 'missing EvidenceAPIView'
assert hasattr(mod, 'EvidenceDetailApiView'), 'missing EvidenceDetailApiView'
assert hasattr(mod, 'LaunchTaskAPIView'), 'missing LaunchTaskAPIView'
