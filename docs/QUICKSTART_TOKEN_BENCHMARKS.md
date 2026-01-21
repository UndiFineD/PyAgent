# Token Generation Speed Testing - Quick Start Guide

## 🎯 What I've Created For You

I've created comprehensive token generation speed testing tools for your PyAgent project:

### 1. **Comprehensive Test Suite** 
`tests/performance/test_token_generation_speed.py` (1000+ lines)

A full-featured benchmarking framework with:
- ✅ Single prompt tests (short, medium, long, code)
- ✅ Streaming performance tests (with vLLM)
- ✅ Batch processing benchmarks
- ✅ Pytest integration
- ✅ JSON output for CI/CD
- ✅ Baseline comparison for regression detection
- ✅ Detailed metrics (tokens/sec, latency, TTFT)

### 2. **Simple Standalone Scripts**

- `scripts/run_benchmarks.py` - Unified command-line benchmark suite (Recommended)
- `scripts/archive/` - Archived legacy benchmark scripts (preserved for reference)

### 3. **Documentation**
`tests/performance/README_TOKEN_SPEED.md`

Complete usage guide with examples, integration patterns, and CI/CD setup.

## 🚀 How to Use

### Unified Benchmark Suite (Fastest)
```bash
python scripts/run_benchmarks.py
```

### Full Pytest Performance Suite (Detailed)
```bash
pytest tests/performance/test_token_generation_speed.py -v -s
```

### Programmatic Access
```python
from src.infrastructure.benchmarks.benchmark_suite import BenchmarkSuite

suite = BenchmarkSuite()
results = suite.run_full_suite()
suite.print_summary()
```

## 📊 What Gets Measured

| Metric | Description |
|--------|-------------|
| **Tokens/sec (total)** | Overall throughput including input + output |
| **Duration (sec)** | Time taken for the test run |
| **Success rate** | Percentage of successful generations |
| **Agent Latency** | End-to-end response time for agents |

## 🎯 Your Next Steps

1. **Run the unified benchmark** (1 minute)
   ```bash
   python scripts/run_benchmarks.py
   ```

2. **Run the pytest performance suite** (5 minutes)
   ```bash
   pytest tests/performance/test_token_generation_speed.py -v -s
   ```

3. **Review results**
   - Check console output for performance metrics
   - Review agent-level latency comparisons

4. **Review legacy tools** (Optional)
   - Archived scripts are available in `scripts/archive/` if needed for historical comparison.

## 📚 Files Created

```
src/infrastructure/benchmarks/
├── benchmark_suite.py     # Unified benchmarking engine
└── models.py              # Shared performance result models

scripts/
└── run_benchmarks.py      # Central CLI entry point

tests/unit/infrastructure/
└── test_benchmark_suite.py # Verification tests
```

## 🤝 Support

If you need help:
1. Check the detailed README: `tests/performance/README_TOKEN_SPEED.md`
2. Review test examples in the pytest file
3. The code is well-commented and self-documenting

## ✨ Summary

You now have:
- ✅ Unified professional-grade benchmarking framework
- ✅ Single entry point for all performance testing
- ✅ Parity testing between Python and Rust tokenization
- ✅ Comprehensive metrics and reporting
- ✅ Async-ready agent performance tracing
- ✅ Full documentation

The PyAgent fleet is now fully instrumented for performance monitoring!

