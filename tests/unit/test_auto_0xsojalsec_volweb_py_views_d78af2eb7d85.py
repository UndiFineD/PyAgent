
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_views_d78af2eb7d85.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'review'), 'missing review'
assert hasattr(mod, 'PsTreeApiView'), 'missing PsTreeApiView'
assert hasattr(mod, 'MFTScanApiView'), 'missing MFTScanApiView'
assert hasattr(mod, 'MBRScanApiView'), 'missing MBRScanApiView'
assert hasattr(mod, 'ADSApiView'), 'missing ADSApiView'
assert hasattr(mod, 'TimelineChartApiView'), 'missing TimelineChartApiView'
assert hasattr(mod, 'TimelineDataApiView'), 'missing TimelineDataApiView'
assert hasattr(mod, 'CmdLineApiView'), 'missing CmdLineApiView'
assert hasattr(mod, 'GetSIDsApiView'), 'missing GetSIDsApiView'
assert hasattr(mod, 'PrivsApiView'), 'missing PrivsApiView'
assert hasattr(mod, 'EnvarsApiView'), 'missing EnvarsApiView'
assert hasattr(mod, 'PsScanApiView'), 'missing PsScanApiView'
assert hasattr(mod, 'DllListApiView'), 'missing DllListApiView'
assert hasattr(mod, 'SessionsApiView'), 'missing SessionsApiView'
assert hasattr(mod, 'NetStatApiView'), 'missing NetStatApiView'
assert hasattr(mod, 'NetScanApiView'), 'missing NetScanApiView'
assert hasattr(mod, 'NetGraphApiView'), 'missing NetGraphApiView'
assert hasattr(mod, 'HiveListApiView'), 'missing HiveListApiView'
assert hasattr(mod, 'SvcScanApiView'), 'missing SvcScanApiView'
assert hasattr(mod, 'HashdumpApiView'), 'missing HashdumpApiView'
assert hasattr(mod, 'CachedumpApiView'), 'missing CachedumpApiView'
assert hasattr(mod, 'LsadumpApiView'), 'missing LsadumpApiView'
assert hasattr(mod, 'MalfindApiView'), 'missing MalfindApiView'
assert hasattr(mod, 'LdrModulesApiView'), 'missing LdrModulesApiView'
assert hasattr(mod, 'ModulesApiView'), 'missing ModulesApiView'
assert hasattr(mod, 'SSDTApiView'), 'missing SSDTApiView'
assert hasattr(mod, 'FileScanApiView'), 'missing FileScanApiView'
assert hasattr(mod, 'HandlesApiView'), 'missing HandlesApiView'
assert hasattr(mod, 'PsListDumpApiView'), 'missing PsListDumpApiView'
assert hasattr(mod, 'FileScanDumpApiView'), 'missing FileScanDumpApiView'
assert hasattr(mod, 'MemmapDumpApiView'), 'missing MemmapDumpApiView'
assert hasattr(mod, 'TasksApiView'), 'missing TasksApiView'
assert hasattr(mod, 'LootApiView'), 'missing LootApiView'
