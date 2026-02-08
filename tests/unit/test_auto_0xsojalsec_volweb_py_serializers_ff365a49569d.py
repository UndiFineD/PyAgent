
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_serializers_ff365a49569d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PsScanSerializer'), 'missing PsScanSerializer'
assert hasattr(mod, 'PsTreeSerializer'), 'missing PsTreeSerializer'
assert hasattr(mod, 'TimelineChartSerializer'), 'missing TimelineChartSerializer'
assert hasattr(mod, 'TimelineDataSerializer'), 'missing TimelineDataSerializer'
assert hasattr(mod, 'TimelineTagSerializer'), 'missing TimelineTagSerializer'
assert hasattr(mod, 'CmdLineSerializer'), 'missing CmdLineSerializer'
assert hasattr(mod, 'GetSIDsSerializer'), 'missing GetSIDsSerializer'
assert hasattr(mod, 'PrivsSerializer'), 'missing PrivsSerializer'
assert hasattr(mod, 'HiveListSerializer'), 'missing HiveListSerializer'
assert hasattr(mod, 'SvcScanSerializer'), 'missing SvcScanSerializer'
assert hasattr(mod, 'EnvarsSerializer'), 'missing EnvarsSerializer'
assert hasattr(mod, 'DllListSerializer'), 'missing DllListSerializer'
assert hasattr(mod, 'SessionsSerializer'), 'missing SessionsSerializer'
assert hasattr(mod, 'NetStatSerializer'), 'missing NetStatSerializer'
assert hasattr(mod, 'NetScanSerializer'), 'missing NetScanSerializer'
assert hasattr(mod, 'NetGraphSerializer'), 'missing NetGraphSerializer'
assert hasattr(mod, 'HashdumpSerializer'), 'missing HashdumpSerializer'
assert hasattr(mod, 'CachedumpSerializer'), 'missing CachedumpSerializer'
assert hasattr(mod, 'LsadumpSerializer'), 'missing LsadumpSerializer'
assert hasattr(mod, 'HandlesSerializer'), 'missing HandlesSerializer'
assert hasattr(mod, 'MalfindSerializer'), 'missing MalfindSerializer'
assert hasattr(mod, 'LdrModulesSerializer'), 'missing LdrModulesSerializer'
assert hasattr(mod, 'ModulesSerializer'), 'missing ModulesSerializer'
assert hasattr(mod, 'SSDTSerializer'), 'missing SSDTSerializer'
assert hasattr(mod, 'FileScanSerializer'), 'missing FileScanSerializer'
assert hasattr(mod, 'MFTScanSerializer'), 'missing MFTScanSerializer'
assert hasattr(mod, 'MBRScanSerializer'), 'missing MBRScanSerializer'
assert hasattr(mod, 'ADSSerializer'), 'missing ADSSerializer'
assert hasattr(mod, 'TasksSerializer'), 'missing TasksSerializer'
assert hasattr(mod, 'LootSerializer'), 'missing LootSerializer'
