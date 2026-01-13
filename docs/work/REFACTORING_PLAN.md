# BaseAgent.py & metrics_engine.py Refactoring Plan
# Phase 4: Large File Decomposition Strategy
# Created: 2026-01-13

## OVERVIEW

Two critical files need Core/Shell decomposition:
1. **BaseAgent.py** (51.2 KB, 1100 lines)
2. **metrics_engine.py** (97.4 KB, 2727 lines)

These are too large for maintainability and contain mixed concerns.

---

## BASEAGENT.PY DECOMPOSITION

### Current Structure Analysis
- **1100 lines** total
- **51.2 KB** file size
- **Main class**: BaseAgent (orchestration + I/O)
- **Key responsibilities**:
  1. Agent state management (properties, lifecycle)
  2. Configuration handling
  3. Capability registration
  4. Command execution (subprocess)
  5. AI backend interaction
  6. File I/O operations
  7. Event hooks and callbacks
  8. Tool registration

### Decomposition Strategy

#### BaseAgentCore (Pure Logic) - ~400 lines
**Location**: `src/core/base/BaseAgentCore.py`
**Responsibility**: All pure logic, zero I/O

Extract these methods/classes:
- `calculate_anchoring_strength()` - Pure calculation
- `verify_self()` - Validation logic
- State validation logic
- Configuration validation logic
- Capability enumeration logic
- Event filtering/routing logic
- Response quality assessment
- Strategy pattern matching

**No imports**: subprocess, requests, file operations, asyncio (except types)

#### BaseAgentShell (I/O Wrapper) - ~700 lines
**Location**: `src/core/base/BaseAgent.py` (keep current name)
**Responsibility**: Orchestration + I/O

Keep in current file:
- `__init__()` - initialization
- `_run_command()` - subprocess execution
- `suspend()` / `resume()` - lifecycle
- AI backend calls
- File I/O operations
- Event hook management
- Tool registration
- Memory management

**Pattern**:
```python
class BaseAgent:
    """Orchestration and I/O shell for agent operations."""
    
    def __init__(self, file_path: str):
        self.core = BaseAgentCore()
        # ... I/O setup
    
    async def execute(self, prompt: str) -> str:
        # Orchestrate core logic + I/O
        quality = self.core.verify_self(result)
        strength = self.core.calculate_anchoring_strength(result)
        # ... save to disk, call APIs, etc
```

### Expected Outcome
- **BaseAgentCore.py**: ~20KB (pure logic)
- **BaseAgent.py**: ~31KB (orchestration + I/O)
- **Rust conversion candidate**: BaseAgentCore ✅

---

## METRICS_ENGINE.PY DECOMPOSITION

### Current Structure Analysis
- **2727 lines** total
- **97.4 KB** file size
- **Main class**: ObservabilityEngine (mixed concerns)
- **Key responsibilities**:
  1. Metric aggregation (pure math)
  2. Time-series calculations
  3. Formula evaluation
  4. Token cost computation
  5. Statistics rollup
  6. File I/O (telemetry persistence)
  7. External exporter integration
  8. Dashboard generation

### Decomposition Strategy

#### MetricsCore (Pure Logic) - ~1000 lines
**Location**: `src/observability/stats/MetricsCore.py`
**Responsibility**: All calculations and aggregations

Extract from metrics_engine.py:
- Token cost calculations (TokenCostCore if not separate)
- Time-series aggregation logic
- Formula evaluation (FormulaEngineCore integration)
- Statistical rollup operations
- Anomaly detection algorithms
- Correlation calculations
- Data structure transformations
- Threshold evaluation logic

**Example classes**:
```python
class MetricsAggregator:
    """Pure calculation of metric aggregations."""
    def rollup(self, metrics: list, interval: str) -> dict: ...
    
class TokenCostCalculator:
    """Token counting and cost computation."""
    def calculate_cost(self, tokens: int, model: str) -> float: ...
    
class TimeSeriesAnalyzer:
    """Statistical analysis of time-series data."""
    def detect_anomalies(self, series: list) -> list: ...
```

**No I/O**: No file operations, subprocess, network calls

#### MetricsEngine (I/O + Orchestration) - ~1700 lines
**Location**: `src/observability/stats/metrics_engine.py` (keep current name)
**Responsibility**: Persistence, export, orchestration

Keep in current file:
- File I/O (telemetry persistence)
- External exporter integration (Prometheus, OTel, Grafana)
- Buffer management
- Database operations
- API calls
- Dashboard generation
- Memory cleanup
- Performance optimization

**Pattern**:
```python
class MetricsEngine:
    """Orchestration and I/O for observability."""
    
    def __init__(self):
        self.core = MetricsCore()
        self.aggregator = MetricsAggregator()
        self.token_calc = TokenCostCalculator()
        # ... exporters
    
    def record_metric(self, metric: AgentMetric) -> None:
        # Calculate using core
        cost = self.token_calc.calculate_cost(...)
        rollup = self.aggregator.rollup(...)
        
        # Persist and export (I/O)
        self._save_telemetry()
        self.prometheus.export(...)
```

### Expected Outcome
- **MetricsCore.py**: ~40KB (pure logic, Rust-convertible)
- **metrics_engine.py**: ~57KB (I/O + orchestration)
- **Rust conversion candidate**: MetricsCore + TokenCostCore ✅

---

## IMPLEMENTATION TIMELINE

### Phase 1: Planning & Analysis (0-2 hours)
- ✅ Identify boundaries between logic and I/O
- ✅ Map class dependencies
- [ ] Document public API contracts
- [ ] Create test stubs

### Phase 2: BaseAgentCore Extraction (4-6 hours)
1. Create BaseAgentCore.py skeleton
2. Extract pure logic methods
3. Update imports
4. Run tests to verify
5. Update BaseAgent to use BaseAgentCore

### Phase 3: MetricsCore Extraction (6-8 hours)
1. Create MetricsCore.py skeleton
2. Extract calculation logic
3. Create TokenCostCore if needed
4. Update imports
5. Run tests to verify
6. Update MetricsEngine to use cores

### Phase 4: Validation & Testing (2-3 hours)
- Run full test suite
- Verify no performance regression
- Validate Rust conversion candidates
- Update documentation

**Total Estimated Time**: 12-19 hours
**Parallelizable**: Phase 2 and 3 can overlap

---

## SUCCESS CRITERIA

### BaseAgent Refactoring
- ✅ BaseAgentCore.py exists and contains only pure logic
- ✅ No I/O imports in BaseAgentCore
- ✅ BaseAgentCore < 25KB
- ✅ All tests pass
- ✅ No functional changes
- ✅ BaseAgentCore ready for Rust conversion

### MetricsEngine Refactoring
- ✅ MetricsCore.py exists (pure logic)
- ✅ TokenCostCore extracted if separate
- ✅ MetricsCore < 50KB
- ✅ All tests pass
- ✅ No functional changes
- ✅ MetricsCore ready for Rust conversion

### Global Outcomes
- ✅ No file >50KB
- ✅ Clear Core/Shell separation in all agents
- ✅ 2 new Rust conversion candidates identified
- ✅ Code maintainability improved
- ✅ Performance maintained or improved

---

## EXECUTION INSTRUCTIONS

### For Manual Implementation

1. **Start with BaseAgent** (smaller, easier)
   ```bash
   # Read current file structure
   # Identify pure logic methods
   # Create BaseAgentCore.py
   # Move methods, update imports
   # Test with: python -m pytest tests/ -k BaseAgent
   ```

2. **Then MetricsEngine** (larger, more complex)
   ```bash
   # Analyze MetricsEngine structure
   # Identify calculation vs I/O code
   # Create MetricsCore.py
   # Move calculation classes
   # Update MetricsEngine imports
   # Test with: python -m pytest tests/ -k metrics
   ```

3. **Validation**
   ```bash
   # Run full test suite
   python -m pytest
   
   # Check file sizes
   ls -lh src/core/base/BaseAgent*
   ls -lh src/observability/stats/Metrics*
   
   # Verify no I/O in Core files
   grep -r "open\|requests\|subprocess\|Path" src/core/base/BaseAgentCore.py
   grep -r "open\|requests\|subprocess\|Path" src/observability/stats/MetricsCore.py
   ```

### For Fleet Script

Update `docs/work/prompt.txt` Phase 4 when starting:
- [ ] Begin BaseAgent.py Core/Shell split
- [ ] Begin MetricsEngine.py Core/Shell split

Mark complete when both files are under 50KB with clear separation.

---

## RISK MITIGATION

### Potential Issues
1. **Circular imports**: Test extensively after split
2. **API compatibility**: Maintain public interfaces
3. **Performance**: Profile before/after
4. **Testing**: Ensure test suite still passes

### Rollback Plan
Keep original files backed up:
```bash
cp src/core/base/BaseAgent.py src/core/base/BaseAgent.py.backup
cp src/observability/stats/metrics_engine.py src/observability/stats/metrics_engine.py.backup
```

If decomposition fails, revert and document blocking issues.

---

## NEXT STEPS

1. ✅ Plan documented
2. ⏳ Ready to begin BaseAgent extraction
3. ⏳ Ready to begin MetricsEngine extraction
4. ⏳ Ready for validation and testing

**Proceed with Phase 2 (BaseAgent extraction)?**
