# Auto-synced test for observability/stats/scheduler_stats.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "scheduler_stats.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MetricExportFormat"), "MetricExportFormat missing"
    assert hasattr(mod, "PrefixCacheStats"), "PrefixCacheStats missing"
    assert hasattr(mod, "SpecDecodingStats"), "SpecDecodingStats missing"
    assert hasattr(mod, "CUDAGraphStats"), "CUDAGraphStats missing"
    assert hasattr(mod, "PerfStats"), "PerfStats missing"
    assert hasattr(mod, "KVCacheEvictionEvent"), "KVCacheEvictionEvent missing"
    assert hasattr(mod, "SchedulerStats"), "SchedulerStats missing"
    assert hasattr(mod, "SchedulerStatsCollector"), "SchedulerStatsCollector missing"
    assert hasattr(mod, "create_scheduler_stats"), "create_scheduler_stats missing"
    assert hasattr(mod, "create_stats_collector"), "create_stats_collector missing"

