# Auto-synced test for infrastructure/services/platform/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PlatformType"), "PlatformType missing"
    assert hasattr(mod, "CpuArchitecture"), "CpuArchitecture missing"
    assert hasattr(mod, "QuantizationType"), "QuantizationType missing"
    assert hasattr(mod, "AttentionBackend"), "AttentionBackend missing"
    assert hasattr(mod, "DeviceFeature"), "DeviceFeature missing"
    assert hasattr(mod, "DeviceCapability"), "DeviceCapability missing"
    assert hasattr(mod, "MemoryInfo"), "MemoryInfo missing"
    assert hasattr(mod, "DeviceInfo"), "DeviceInfo missing"
    assert hasattr(mod, "PlatformConfig"), "PlatformConfig missing"

