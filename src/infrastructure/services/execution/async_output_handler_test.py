# Auto-synced test for infrastructure/services/execution/async_output_handler.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "async_output_handler.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AsyncState"), "AsyncState missing"
    assert hasattr(mod, "CudaEvent"), "CudaEvent missing"
    assert hasattr(mod, "CudaStream"), "CudaStream missing"
    assert hasattr(mod, "AsyncOutput"), "AsyncOutput missing"
    assert hasattr(mod, "async_copy_to_np"), "async_copy_to_np missing"
    assert hasattr(mod, "async_copy_batch"), "async_copy_batch missing"
    assert hasattr(mod, "AsyncBarrier"), "AsyncBarrier missing"
    assert hasattr(mod, "async_barrier"), "async_barrier missing"
    assert hasattr(mod, "AsyncOutputHandler"), "AsyncOutputHandler missing"
    assert hasattr(mod, "DoubleBuffer"), "DoubleBuffer missing"

