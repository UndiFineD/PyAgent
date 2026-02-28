# Splice: src/observability/stats/analysis.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ProfileStats
- ProfilingCore
- FleetMetrics
- StabilityCore
- TracingCore
- DerivedMetricCalculator
- CorrelationAnalyzer
- FormulaEngineCore
- FormulaEngine
- TokenCostCore
- TokenCostEngine
- ModelFallbackCore
- ModelFallbackEngine
- StatsRollupCalculator
- StatsForecaster
- ABComparator
- ResourceMonitor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
