
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_volweb_py_serializers_f6dc697deb6d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PsTreeSerializer'), 'missing PsTreeSerializer'
assert hasattr(mod, 'PsAuxSerializer'), 'missing PsAuxSerializer'
assert hasattr(mod, 'LsofSerializer'), 'missing LsofSerializer'
assert hasattr(mod, 'EnvarsSerializer'), 'missing EnvarsSerializer'
assert hasattr(mod, 'PsScanSerializer'), 'missing PsScanSerializer'
assert hasattr(mod, 'MountInfoSerializer'), 'missing MountInfoSerializer'
assert hasattr(mod, 'tty_checkSerializer'), 'missing tty_checkSerializer'
assert hasattr(mod, 'BashSerializer'), 'missing BashSerializer'
assert hasattr(mod, 'ElfsSerializer'), 'missing ElfsSerializer'
assert hasattr(mod, 'MalfindSerializer'), 'missing MalfindSerializer'
assert hasattr(mod, 'LsmodSerializer'), 'missing LsmodSerializer'
assert hasattr(mod, 'CapabilitiesSerializer'), 'missing CapabilitiesSerializer'
assert hasattr(mod, 'KmsgSerializer'), 'missing KmsgSerializer'
assert hasattr(mod, 'NetGraphSerializer'), 'missing NetGraphSerializer'
assert hasattr(mod, 'TimelineChartSerializer'), 'missing TimelineChartSerializer'
assert hasattr(mod, 'TimelineDataSerializer'), 'missing TimelineDataSerializer'
