
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_boring_classes_eec81343e1ed.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RandomDictDataset'), 'missing RandomDictDataset'
assert hasattr(mod, 'RandomDataset'), 'missing RandomDataset'
assert hasattr(mod, 'RandomIterableDataset'), 'missing RandomIterableDataset'
assert hasattr(mod, 'RandomIterableDatasetWithLen'), 'missing RandomIterableDatasetWithLen'
assert hasattr(mod, 'BoringModel'), 'missing BoringModel'
assert hasattr(mod, 'BoringDataModule'), 'missing BoringDataModule'
assert hasattr(mod, 'BoringDataModuleNoLen'), 'missing BoringDataModuleNoLen'
assert hasattr(mod, 'IterableBoringDataModule'), 'missing IterableBoringDataModule'
assert hasattr(mod, 'ManualOptimBoringModel'), 'missing ManualOptimBoringModel'
assert hasattr(mod, 'DemoModel'), 'missing DemoModel'
assert hasattr(mod, 'Net'), 'missing Net'
