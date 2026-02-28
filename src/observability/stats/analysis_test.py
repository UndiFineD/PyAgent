# Auto-synced test for observability/stats/analysis.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "analysis.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ProfileStats"), "ProfileStats missing"
    assert hasattr(mod, "ProfilingCore"), "ProfilingCore missing"
    assert hasattr(mod, "FleetMetrics"), "FleetMetrics missing"
    assert hasattr(mod, "StabilityCore"), "StabilityCore missing"
    assert hasattr(mod, "TracingCore"), "TracingCore missing"
    assert hasattr(mod, "DerivedMetricCalculator"), "DerivedMetricCalculator missing"
    assert hasattr(mod, "CorrelationAnalyzer"), "CorrelationAnalyzer missing"
    assert hasattr(mod, "FormulaEngineCore"), "FormulaEngineCore missing"
    assert hasattr(mod, "FormulaEngine"), "FormulaEngine missing"
    assert hasattr(mod, "TokenCostCore"), "TokenCostCore missing"
    assert hasattr(mod, "TokenCostEngine"), "TokenCostEngine missing"
    assert hasattr(mod, "ModelFallbackCore"), "ModelFallbackCore missing"
    assert hasattr(mod, "ModelFallbackEngine"), "ModelFallbackEngine missing"
    assert hasattr(mod, "StatsRollupCalculator"), "StatsRollupCalculator missing"
    assert hasattr(mod, "StatsForecaster"), "StatsForecaster missing"
    assert hasattr(mod, "ABComparator"), "ABComparator missing"
    assert hasattr(mod, "ResourceMonitor"), "ResourceMonitor missing"

