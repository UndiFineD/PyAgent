# Auto-synced test for infrastructure/services/platform/platform_interface.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "platform_interface.py"
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
    assert hasattr(mod, "Platform"), "Platform missing"
    assert hasattr(mod, "CudaPlatform"), "CudaPlatform missing"
    assert hasattr(mod, "RocmPlatform"), "RocmPlatform missing"
    assert hasattr(mod, "TpuPlatform"), "TpuPlatform missing"
    assert hasattr(mod, "XpuPlatform"), "XpuPlatform missing"
    assert hasattr(mod, "CpuPlatform"), "CpuPlatform missing"
    assert hasattr(mod, "PlatformRegistry"), "PlatformRegistry missing"
    assert hasattr(mod, "get_current_platform"), "get_current_platform missing"
    assert hasattr(mod, "detect_platform"), "detect_platform missing"
    assert hasattr(mod, "get_device_count"), "get_device_count missing"
    assert hasattr(mod, "get_device_capability"), "get_device_capability missing"
    assert hasattr(mod, "get_memory_info"), "get_memory_info missing"
    assert hasattr(mod, "is_quantization_supported"), "is_quantization_supported missing"
    assert hasattr(mod, "select_attention_backend"), "select_attention_backend missing"

