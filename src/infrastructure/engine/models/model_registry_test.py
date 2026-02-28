# Auto-synced test for infrastructure/engine/models/model_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "model_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "register_model"), "register_model missing"
    assert hasattr(mod, "get_model_info"), "get_model_info missing"
    assert hasattr(mod, "detect_architecture"), "detect_architecture missing"
    assert hasattr(mod, "estimate_vram"), "estimate_vram missing"
    assert hasattr(mod, "ModelCapability"), "ModelCapability missing"
    assert hasattr(mod, "ModelArchitecture"), "ModelArchitecture missing"
    assert hasattr(mod, "QuantizationType"), "QuantizationType missing"
    assert hasattr(mod, "ModelFormat"), "ModelFormat missing"
    assert hasattr(mod, "ModelConfig"), "ModelConfig missing"
    assert hasattr(mod, "ArchitectureSpec"), "ArchitectureSpec missing"
    assert hasattr(mod, "ModelInfo"), "ModelInfo missing"
    assert hasattr(mod, "VRAMEstimate"), "VRAMEstimate missing"
    assert hasattr(mod, "ArchitectureDetector"), "ArchitectureDetector missing"
    assert hasattr(mod, "VRAMEstimator"), "VRAMEstimator missing"
    assert hasattr(mod, "ModelRegistry"), "ModelRegistry missing"

