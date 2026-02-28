# Auto-synced test for infrastructure/compute/quantization/quantization_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "quantization_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "QuantScheme"), "QuantScheme missing"
    assert hasattr(mod, "QuantStrategy"), "QuantStrategy missing"
    assert hasattr(mod, "QuantConfig"), "QuantConfig missing"
    assert hasattr(mod, "QuantizedTensor"), "QuantizedTensor missing"
    assert hasattr(mod, "Quantizer"), "Quantizer missing"
    assert hasattr(mod, "LinearQuantizer"), "LinearQuantizer missing"
    assert hasattr(mod, "AWQQuantizer"), "AWQQuantizer missing"
    assert hasattr(mod, "GPTQQuantizer"), "GPTQQuantizer missing"
    assert hasattr(mod, "DequantizedLinear"), "DequantizedLinear missing"
    assert hasattr(mod, "pack_int4"), "pack_int4 missing"
    assert hasattr(mod, "unpack_int4"), "unpack_int4 missing"
    assert hasattr(mod, "compute_scales_minmax"), "compute_scales_minmax missing"
    assert hasattr(mod, "quantize_tensor"), "quantize_tensor missing"
    assert hasattr(mod, "get_quantization_error"), "get_quantization_error missing"

