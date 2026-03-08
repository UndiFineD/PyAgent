#!/usr/bin/env python3
"""Auto-synced test for observability/telemetry/usage_message.py."""
# Auto-synced test for observability/telemetry/usage_message.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the module under test without importing it at the top level."""
    p = pathlib.Path(__file__).parent / "usage_message.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise ValueError(f"Failed to load spec from {p}")
    if spec.loader is None:
        raise ValueError(f"Failed to load loader from {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the usage_message module can be loaded and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "UsageContext"), "UsageContext missing"
    assert hasattr(mod, "set_runtime_usage_data"), "set_runtime_usage_data missing"
    assert hasattr(mod, "get_runtime_usage_data"), "get_runtime_usage_data missing"
    assert hasattr(mod, "clear_runtime_usage_data"), "clear_runtime_usage_data missing"
    assert hasattr(mod, "is_usage_stats_enabled"), "is_usage_stats_enabled missing"
    assert hasattr(mod, "disable_usage_stats"), "disable_usage_stats missing"
    assert hasattr(mod, "enable_usage_stats"), "enable_usage_stats missing"
    assert hasattr(mod, "detect_cloud_provider"), "detect_cloud_provider missing"
    assert hasattr(mod, "get_cpu_info"), "get_cpu_info missing"
    assert hasattr(mod, "get_gpu_info"), "get_gpu_info missing"
    assert hasattr(mod, "get_memory_info"), "get_memory_info missing"
    assert hasattr(mod, "UsageMessage"), "UsageMessage missing"
    assert hasattr(mod, "report_usage"), "report_usage missing"
    assert hasattr(mod, "get_platform_summary"), "get_platform_summary missing"
