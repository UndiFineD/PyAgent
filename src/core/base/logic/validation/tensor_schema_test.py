# Auto-synced test for core/base/logic/validation/tensor_schema.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "tensor_schema.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TensorShape"), "TensorShape missing"
    assert hasattr(mod, "TensorSchema"), "TensorSchema missing"
    assert hasattr(mod, "validate_tensor"), "validate_tensor missing"
    assert hasattr(mod, "validate_tensor_shape"), "validate_tensor_shape missing"
    assert hasattr(mod, "DynamicDim"), "DynamicDim missing"

