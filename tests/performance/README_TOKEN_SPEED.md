# Token Generation Speed Testing for PyAgent

This directory contains comprehensive tools for testing and benchmarking token generation speed in PyAgent.

## Quick Start

### Option 1: Unified Benchmark Script (Recommended)

Run the unified benchmark script for high-speed infrastructure testing:

```bash
python scripts/run_benchmarks.py
```

This will:
- Run tokenization benchmarks (Python vs Rust)
- Measure sustained throughput for 10 seconds
- Trace agent-level latency using `BenchmarkAgent`
- Display a consolidated performance summary

### Option 2: Comprehensive Test Suite

Run the full pytest-based benchmark suite for detailed LLM generation analysis:

```bash
# Run all performance tests
pytest tests/performance/test_token_generation_speed.py -v

# Run with detailed output
pytest tests/performance/test_token_generation_speed.py -v -s
```

### Option 3: Unified Infrastructure API

```python
from src.infrastructure.benchmarks.benchmark_suite import BenchmarkSuite

# Create benchmark suite instance
suite = BenchmarkSuite()

# Run all benchmarks
results = suite.run_all()

# Print summary to console
suite.print_summary()
```

## What Gets Tested

### 1. Single Prompt Tests
- **Short prompts**: Basic questions (~10-20 tokens)
- **Medium prompts**: Detailed questions (~50-100 tokens)
- **Long prompts**: Complex analysis requests (~200+ tokens)
- **Code generation**: Programming tasks

### 2. Streaming Tests
- Token-by-token streaming performance
- Time to first token (TTFT)
- Streaming throughput vs batch throughput
- Works with vLLM backend when available

### 3. Batch Processing Tests
- Batch sizes: 5, 10, 20 prompts
- Throughput comparison vs single requests
- Resource utilization patterns

## Key Metrics Measured

### Performance Metrics
- **Tokens/sec (total)**: Overall throughput including input + output
- **Tokens/sec (output only)**: Generation speed for output tokens only
- **Latency per token (ms)**: Time taken per token generated
- **Time to first token (TTFT)**: Streaming latency metric
- **Total duration**: End-to-end request time

### Quality Metrics
- **Success rate**: Percentage of successful generations
- **Error tracking**: Detailed error messages for failures
- **Model/backend info**: What configuration was used

## Output Format

### Console Output
The benchmark provides rich formatted output with:
- Real-time progress indicators
- Per-test results with emoji indicators (✅/❌)
- Summary statistics with averages
- Performance by backend comparison
- Best/worst performance highlighting

### JSON Output
Results are saved to JSON files with structure:
```json
{
  "timestamp": 1234567890.123,
  "total_tests": 12,
  "successful_tests": 11,
  "failed_tests": 1,
  "results": [
    {
      "test_name": "single_short",
      "backend": "github-models",
      "model_name": "gpt-4o",
      "total_duration_sec": 1.234,
      "tokens_per_second": 45.67,
      "total_tokens": 56,
      "input_tokens": 10,
      "output_tokens": 46,
      "success": true,
      ...
    }
  ]
}
```

## Baseline Comparison

Compare current performance against a baseline:

```python
# Run new benchmark
benchmark = TokenGenerationBenchmark()
benchmark.run_all_tests(agent)
benchmark.save_results("current.json")

# Compare with previous baseline
comparison = benchmark.compare_with_baseline(
    Path("tests/performance/results/baseline.json")
)

# Check for regression
if comparison.get("regression"):
    print("⚠️ PERFORMANCE REGRESSION DETECTED!")
    print(f"Slower by {abs(comparison['improvement_percent']):.1f}%")
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Token Speed Benchmark

on: [push, pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements/base.txt
          pip install -r requirements/dev.txt
      
      - name: Run token speed benchmark
        run: |
          python scripts/benchmark_token_speed.py
      
      - name: Run pytest benchmarks
        run: |
          pytest tests/performance/test_token_generation_speed.py -v
      
      - name: Check for regression
        run: |
          python -c "
          from tests.performance.test_token_generation_speed import TokenGenerationBenchmark
          from pathlib import Path
          
          benchmark = TokenGenerationBenchmark()
          comparison = benchmark.compare_with_baseline(
              Path('tests/performance/results/baseline.json')
          )
          
          if comparison.get('regression'):
              exit(1)  # Fail CI if regression detected
          "
```

## Advanced Usage

### Custom Agent Testing

Test your own custom agent:

```python
from tests.performance.test_token_generation_speed import TokenGenerationBenchmark

# Your custom agent
from src.logic.agents.custom.MyAgent import MyAgent

benchmark = TokenGenerationBenchmark()
my_agent = MyAgent("path/to/config")

# Run single test
result = benchmark.measure_agent_generation_speed(
    agent=my_agent,
    prompt="Your custom prompt here",
    test_name="custom_test",
    max_tokens=500,
)

print(f"Tokens/sec: {result.tokens_per_second:.2f}")
```

### Custom Prompts

```python
benchmark = TokenGenerationBenchmark()

# Add custom prompts
benchmark.test_prompts["scientific"] = (
    "Explain quantum entanglement and its implications for quantum computing."
)

benchmark.test_prompts["creative"] = (
    "Write a short story about an AI learning to appreciate art."
)

# Run tests with custom prompts
results = benchmark.run_single_prompt_tests(agent)
```

### Batch Size Experiments

```python
# Test various batch sizes
batch_sizes = [1, 2, 5, 10, 20, 50, 100]
results = benchmark.run_batch_tests(agent, batch_sizes=batch_sizes)

# Analyze scaling
for result in results:
    throughput_per_item = result.tokens_per_second / result.batch_size
    print(f"Batch {result.batch_size}: {throughput_per_item:.2f} tokens/sec/item")
```

### Backend Comparison

```python
# Test different backends
backends = ["github-models", "vllm", "ollama"]

for backend in backends:
    agent.backend = backend
    
    result = benchmark.measure_agent_generation_speed(
        agent=agent,
        prompt="Test prompt",
        test_name=f"backend_{backend}",
    )
    
    print(f"{backend}: {result.tokens_per_second:.2f} tokens/sec")
```

## Troubleshooting

### vLLM Not Available
If streaming tests are skipped:
```bash
# Install vLLM (requires CUDA)
pip install vllm

# Or run without streaming tests
benchmark.run_all_tests(agent, include_streaming=False)
```

### Rust Core Not Available
If you see warnings about Rust acceleration:
```bash
# Build Rust core
cd rust_core
cargo build --release
cp target/release/rust_core.pyd ..
```

### Agent Methods Not Found
If the benchmark can't find agent methods, ensure your agent implements:
- `improve_content(prompt: str) -> str`, or
- `chat(prompt: str) -> str`, or
- `run_benchmark(agent_name: str, task: str) -> str`

## Performance Targets

### Expected Performance (2026 Baseline)

| Model Type | Tokens/sec | Latency/token |
|------------|-----------|---------------|
| GPT-4o | 40-60 | 16-25ms |
| GPT-3.5-turbo | 80-120 | 8-12ms |
| Claude Sonnet | 50-70 | 14-20ms |
| Local vLLM (A100) | 100-200 | 5-10ms |
| Local vLLM (RTX 4090) | 50-100 | 10-20ms |

These are rough estimates and will vary based on:
- Model size
- Hardware specs
- Batch size
- Prompt complexity
- Network latency (for API models)

## Files

- `test_token_generation_speed.py`: Comprehensive pytest-based benchmark suite
- `scripts/benchmark_token_speed.py`: Simple standalone script
- `results/`: Directory for JSON output files
- `results/baseline.json`: Reference baseline for regression testing

## Related Documentation

- [Architecture](../../docs/ARCHITECTURE.md)
- [Performance Guide](../../docs/IMPROVEMENT_RESEARCH.md)
- [vLLM Comparison](../../docs/comparison_vllm.md)

## Contributing

To add new benchmark tests:

1. Add new test methods to `TokenGenerationBenchmark` class
2. Follow naming convention: `test_*` for pytest discovery
3. Use `TokenGenMetrics` dataclass for consistent results
4. Update this README with new test descriptions

## License

Copyright 2026 PyAgent Authors. Licensed under Apache 2.0.
