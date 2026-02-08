
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_lstm_b55a3d23b182.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SimpleLSTM'), 'missing SimpleLSTM'
assert hasattr(mod, 'SequenceSampler'), 'missing SequenceSampler'
assert hasattr(mod, 'LightningLSTM'), 'missing LightningLSTM'
