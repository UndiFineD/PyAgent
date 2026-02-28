# Auto-synced test for infrastructure/engine/loading/weight_loader.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "weight_loader.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "WeightFormat"), "WeightFormat missing"
    assert hasattr(mod, "WeightSpec"), "WeightSpec missing"
    assert hasattr(mod, "LoadStats"), "LoadStats missing"
    assert hasattr(mod, "AtomicWriter"), "AtomicWriter missing"
    assert hasattr(mod, "atomic_writer"), "atomic_writer missing"
    assert hasattr(mod, "detect_weight_format"), "detect_weight_format missing"
    assert hasattr(mod, "get_file_lock_path"), "get_file_lock_path missing"
    assert hasattr(mod, "WeightLoader"), "WeightLoader missing"
    assert hasattr(mod, "SafetensorsLoader"), "SafetensorsLoader missing"
    assert hasattr(mod, "MultiThreadWeightLoader"), "MultiThreadWeightLoader missing"
    assert hasattr(mod, "FastSafetensorsLoader"), "FastSafetensorsLoader missing"
    assert hasattr(mod, "StreamingWeightLoader"), "StreamingWeightLoader missing"
    assert hasattr(mod, "compute_weight_hash_rust"), "compute_weight_hash_rust missing"
    assert hasattr(mod, "validate_weight_shapes_rust"), "validate_weight_shapes_rust missing"
    assert hasattr(mod, "filter_shared_tensors"), "filter_shared_tensors missing"

