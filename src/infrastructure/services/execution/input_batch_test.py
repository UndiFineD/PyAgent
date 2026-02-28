# Auto-synced test for infrastructure/services/execution/input_batch.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "input_batch.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SamplingMetadata"), "SamplingMetadata missing"
    assert hasattr(mod, "InputBuffers"), "InputBuffers missing"
    assert hasattr(mod, "InputBatch"), "InputBatch missing"
    assert hasattr(mod, "BatchBuilder"), "BatchBuilder missing"

