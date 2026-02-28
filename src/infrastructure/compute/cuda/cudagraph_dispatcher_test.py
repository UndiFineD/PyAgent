# Auto-synced test for infrastructure/compute/cuda/cudagraph_dispatcher.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cudagraph_dispatcher.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DispatchMode"), "DispatchMode missing"
    assert hasattr(mod, "DispatchKey"), "DispatchKey missing"
    assert hasattr(mod, "DispatchStats"), "DispatchStats missing"
    assert hasattr(mod, "DispatchPolicy"), "DispatchPolicy missing"
    assert hasattr(mod, "DefaultDispatchPolicy"), "DefaultDispatchPolicy missing"
    assert hasattr(mod, "AdaptiveDispatchPolicy"), "AdaptiveDispatchPolicy missing"
    assert hasattr(mod, "GraphEntry"), "GraphEntry missing"
    assert hasattr(mod, "CudagraphDispatcher"), "CudagraphDispatcher missing"
    assert hasattr(mod, "CompositeDispatcher"), "CompositeDispatcher missing"
    assert hasattr(mod, "StreamDispatcher"), "StreamDispatcher missing"
    assert hasattr(mod, "create_dispatch_key"), "create_dispatch_key missing"
    assert hasattr(mod, "get_padded_key"), "get_padded_key missing"

