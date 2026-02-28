# Auto-synced test for infrastructure/engine/models/registry/config.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ModelCapability"), "ModelCapability missing"
    assert hasattr(mod, "ModelArchitecture"), "ModelArchitecture missing"
    assert hasattr(mod, "QuantizationType"), "QuantizationType missing"
    assert hasattr(mod, "ModelFormat"), "ModelFormat missing"
    assert hasattr(mod, "ModelConfig"), "ModelConfig missing"
    assert hasattr(mod, "ArchitectureSpec"), "ArchitectureSpec missing"
    assert hasattr(mod, "ModelInfo"), "ModelInfo missing"
    assert hasattr(mod, "VRAMEstimate"), "VRAMEstimate missing"

