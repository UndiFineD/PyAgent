# Auto-synced test for observability/logging/enhanced_logger.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "enhanced_logger.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LogScopeEnum"), "LogScopeEnum missing"
    assert hasattr(mod, "debug_once"), "debug_once missing"
    assert hasattr(mod, "info_once"), "info_once missing"
    assert hasattr(mod, "warning_once"), "warning_once missing"
    assert hasattr(mod, "error_once"), "error_once missing"
    assert hasattr(mod, "patch_logger"), "patch_logger missing"
    assert hasattr(mod, "init_logger"), "init_logger missing"
    assert hasattr(mod, "EnhancedLoggerAdapter"), "EnhancedLoggerAdapter missing"
    assert hasattr(mod, "create_enhanced_logger"), "create_enhanced_logger missing"
    assert hasattr(mod, "clear_dedup_cache"), "clear_dedup_cache missing"
    assert hasattr(mod, "get_dedup_cache_info"), "get_dedup_cache_info missing"
    assert hasattr(mod, "EnhancedLogger"), "EnhancedLogger missing"

