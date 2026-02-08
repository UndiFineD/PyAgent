
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_positionwise_feed_forward_9c6f0b94d5e4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PositionwiseFeedForward'), 'missing PositionwiseFeedForward'
assert hasattr(mod, 'MoEFFNLayer'), 'missing MoEFFNLayer'
