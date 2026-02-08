
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_serializers_e678e772130a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EvidenceSerializer'), 'missing EvidenceSerializer'
assert hasattr(mod, 'AnalysisStartSerializer'), 'missing AnalysisStartSerializer'
