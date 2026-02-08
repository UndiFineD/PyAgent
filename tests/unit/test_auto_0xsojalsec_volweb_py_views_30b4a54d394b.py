
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_views_30b4a54d394b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'home'), 'missing home'
assert hasattr(mod, 'websocket_url'), 'missing websocket_url'
assert hasattr(mod, 'minio_secrets'), 'missing minio_secrets'
assert hasattr(mod, 'statistics'), 'missing statistics'
assert hasattr(mod, 'IndicatorApiView'), 'missing IndicatorApiView'
assert hasattr(mod, 'IndicatorEvidenceApiView'), 'missing IndicatorEvidenceApiView'
assert hasattr(mod, 'IndicatorCaseApiView'), 'missing IndicatorCaseApiView'
assert hasattr(mod, 'IndicatorExportApiView'), 'missing IndicatorExportApiView'
