
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_task_channel_d36c9c21991d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PacketStatus'), 'missing PacketStatus'
assert hasattr(mod, 'Packet'), 'missing Packet'
assert hasattr(mod, 'TaskChannel'), 'missing TaskChannel'
