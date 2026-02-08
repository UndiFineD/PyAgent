
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_views_fea420b9bc8f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'review'), 'missing review'
assert hasattr(mod, 'PsTreeApiView'), 'missing PsTreeApiView'
assert hasattr(mod, 'PsAuxApiView'), 'missing PsAuxApiView'
assert hasattr(mod, 'LsofApiView'), 'missing LsofApiView'
assert hasattr(mod, 'ElfsApiView'), 'missing ElfsApiView'
assert hasattr(mod, 'EnvarsApiView'), 'missing EnvarsApiView'
assert hasattr(mod, 'CapabilitiesApiView'), 'missing CapabilitiesApiView'
assert hasattr(mod, 'PsScanApiView'), 'missing PsScanApiView'
assert hasattr(mod, 'tty_checkApiView'), 'missing tty_checkApiView'
assert hasattr(mod, 'MountInfoApiView'), 'missing MountInfoApiView'
assert hasattr(mod, 'KmsgApiView'), 'missing KmsgApiView'
assert hasattr(mod, 'MalfindApiView'), 'missing MalfindApiView'
assert hasattr(mod, 'LsmodApiView'), 'missing LsmodApiView'
assert hasattr(mod, 'SockstatApiView'), 'missing SockstatApiView'
assert hasattr(mod, 'NetGraphApiView'), 'missing NetGraphApiView'
assert hasattr(mod, 'BashApiView'), 'missing BashApiView'
assert hasattr(mod, 'TimelineChartApiView'), 'missing TimelineChartApiView'
assert hasattr(mod, 'TimelineDataApiView'), 'missing TimelineDataApiView'
