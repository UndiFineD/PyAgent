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

<<<<<<< HEAD
- `scripts/benchmark_token_speed.py` - User-friendly command-line benchmark
- `scripts/simple_token_bench.py` - Infrastructure testing without full agent
- `scripts/rust_token_bench.py` - Direct Rust core performance testing
=======
- `scripts/run_benchmarks.py` - Unified command-line benchmark suite (Recommended)
- `scripts/archive/` - Archived legacy benchmark scripts (preserved for reference)
>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)

### 3. **Documentation**
`tests/performance/README_TOKEN_SPEED.md`

Complete usage guide with examples, integration patterns, and CI/CD setup.

<<<<<<< HEAD
## ⚠️ Current Issues Identified

### Import Problem
Your codebase has an import inconsistency:
- Files import: `from src.core.base.Version import VERSION`
- Actual file: `src/core/base/version.py` (lowercase 'v')

**Fix needed:**
```bash
# Option 1: Rename the file
mv src/core/base/version.py src/core/base/Version.py

# Option 2: Fix all imports (safer)
# Change: from src.core.base.Version import VERSION
# To:     from src.core.base.version import VERSION
```

### Rust Core Dependencies
The `rust_core.pyd` exists but has missing DLL dependencies. This is a Windows DLL linkage issue.

## 🚀 How to Use (Once Fixed)

### Quick Test (Recommended)
```bash
python scripts/benchmark_token_speed.py
```

### Full Pytest Suite
=======
## 🚀 How to Use

### Unified Benchmark Suite (Fastest)
```bash
python scripts/run_benchmarks.py
```

### Full Pytest Performance Suite (Detailed)
>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)
```bash
pytest tests/performance/test_token_generation_speed.py -v -s
```

<<<<<<< HEAD
### Python API
```python
from tests.performance.test_token_generation_speed import TokenGenerationBenchmark

benchmark = TokenGenerationBenchmark()
results = benchmark.run_all_tests()
benchmark.print_summary()
benchmark.save_results("my_benchmark.json")
=======
### Programmatic Access
```python
from src.infrastructure.benchmarks.benchmark_suite import BenchmarkSuite

suite = BenchmarkSuite()
results = suite.run_full_suite()
suite.print_summary()
>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)
```

## 📊 What Gets Measured

| Metric | Description |
|--------|-------------|
| **Tokens/sec (total)** | Overall throughput including input + output |
<<<<<<< HEAD
| **Tokens/sec (output)** | Generation speed for output tokens only |
| **Latency/token (ms)** | Time per token generated |
| **TTFT (sec)** | Time to first token (streaming) |
| **Success rate** | Percentage of successful generations |

## 🔧 Quick Fix Instructions

### Step 1: Fix Import Issue
```bash
# Create a simple fix script
cat > fix_imports.py << 'EOF'
import os
from pathlib import Path

# Rename version.py to Version.py
version_file = Path("src/core/base/version.py")
if version_file.exists():
    version_file.rename("src/core/base/Version.py")
    print("✅ Renamed version.py to Version.py")
else:
    print("⚠️ version.py not found")
EOF

python fix_imports.py
```

### Step 2: Test Infrastructure
```bash
# Try the simple benchmark first
python scripts/simple_token_bench.py
```

### Step 3: Run Full Benchmark
```bash
python scripts/benchmark_token_speed.py
```

## 📈 Expected Output Example

```
🚀 PyAgent Token Generation Speed Benchmark Suite
======================================================================

📝 Running single prompt tests...

✅ single_short
   Model: gpt-4o
   Tokens/sec: 45.67
   Output tokens/sec: 38.23
   Latency/token: 26.14ms
   Total tokens: 56 (in: 10, out: 46)
   Duration: 1.226s

✅ single_medium
   Model: gpt-4o
   Tokens/sec: 52.31
   ...

📊 BENCHMARK SUMMARY
======================================================================

🎯 Average Performance:
   Tokens/sec (total): 48.92
   Tokens/sec (output only): 41.15
   Latency/token: 24.33ms

🏆 Best Performance:
   Test: single_medium
   Model: gpt-4o
   Tokens/sec: 52.31
```

## 🎯 Your Next Steps

1. **Fix the import issue** (5 minutes)
   - Rename `src/core/base/version.py` to `Version.py`, OR
   - Use find/replace to fix imports across codebase

2. **Test basic functionality** (2 minutes)
   ```bash
   python scripts/simple_token_bench.py
   ```

3. **Run full benchmark** (5-10 minutes)
   ```bash
   python scripts/benchmark_token_speed.py
   ```

4. **Review results**
   - Check console output for performance metrics
   - Look for JSON file in `tests/performance/results/`

5. **Set performance baselines**
   ```bash
   # Save current as baseline
   cp tests/performance/results/token_generation_benchmark.json \\
      tests/performance/results/baseline.json
   ```

6. **Integrate with CI/CD** (optional)
   - See `README_TOKEN_SPEED.md` for GitHub Actions example
   - Set up regression alerts

## 💡 Alternative: Test Without Agent

If you can't fix imports immediately, you can still test tokenization:

```python
# Create test_tokenization_only.py
import rust_core  # If available

text = "Your test prompt here"
tokens = rust_core.estimate_tokens_rust(text)
print(f"Tokens: {tokens}")
```
=======
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
>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)

## 📚 Files Created

```
<<<<<<< HEAD
tests/performance/
├── test_token_generation_speed.py    # Main pytest suite (1000+ lines)
├── README_TOKEN_SPEED.md             # Complete documentation
└── results/                          # Output directory (auto-created)

scripts/
├── benchmark_token_speed.py          # Simple standalone benchmark
├── simple_token_bench.py             # Infrastructure test
└── rust_token_bench.py               # Rust-only benchmark
=======
src/infrastructure/benchmarks/
├── benchmark_suite.py     # Unified benchmarking engine
└── models.py              # Shared performance result models

scripts/
└── run_benchmarks.py      # Central CLI entry point

tests/unit/infrastructure/
└── test_benchmark_suite.py # Verification tests
>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)
```

## 🤝 Support

If you need help:
1. Check the detailed README: `tests/performance/README_TOKEN_SPEED.md`
2. Review test examples in the pytest file
3. The code is well-commented and self-documenting

## ✨ Summary

You now have:
<<<<<<< HEAD
- ✅ Professional-grade benchmarking framework
- ✅ Multiple testing approaches (pytest, standalone, API)
- ✅ Comprehensive metrics and reporting
- ✅ CI/CD integration examples
- ✅ Baseline comparison for regression testing
- ✅ Full documentation

Once you fix the import issue, you'll be able to run comprehensive token generation speed tests on your PyAgent!
=======
- ✅ Unified professional-grade benchmarking framework
- ✅ Single entry point for all performance testing
- ✅ Parity testing between Python and Rust tokenization
- ✅ Comprehensive metrics and reporting
- ✅ Async-ready agent performance tracing
- ✅ Full documentation

The PyAgent fleet is now fully instrumented for performance monitoring!

>>>>>>> a868309cb (feat(rust_core): refactor to modular registration and modernize PyO3 API)
