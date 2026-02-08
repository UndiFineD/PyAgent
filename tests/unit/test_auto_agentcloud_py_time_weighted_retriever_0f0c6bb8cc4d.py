
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_time_weighted_retriever_0f0c6bb8cc4d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_get_hours_passed'), 'missing _get_hours_passed'
assert hasattr(mod, 'CustomTimeWeightedVectorStoreRetriever'), 'missing CustomTimeWeightedVectorStoreRetriever'
