#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Token Generation Speed Benchmarking Suite for PyAgent.

Tests various aspects of token generation performance:
- Single agent response speed
- Streaming vs non-streaming performance
- Multi-agent orchestration throughput
- Backend comparison (vLLM, GitHub Models, etc.)
- Token-per-second metrics with different model sizes
"""

from __future__ import annotations

import asyncio
import json
import statistics
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

import pytest

# Core imports
try:
    from src.core.base.lifecycle.base_agent import BaseAgent
    from src.logic.agents.analysis.benchmark_agent import BenchmarkAgent
    from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import (
        StreamingVllmEngine,
        StreamingConfig,
        TokenStreamIterator,
    )
    from src.infrastructure.engine.tokenization.tokenizer_registry import estimate_token_count

    HAS_PYAGENT = True
except ImportError:
    HAS_PYAGENT = False

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


@dataclass
class TokenGenMetrics:
    """Comprehensive token generation metrics."""

    test_name: str
    backend: str
    model_name: str

    # Timing metrics
    total_duration_sec: float
    time_to_first_token_sec: Optional[float] = None

    # Token metrics
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0

    # Derived metrics
    tokens_per_second: float = 0.0
    tokens_per_second_output_only: float = 0.0
    latency_per_token_ms: float = 0.0

    # Quality metrics
    success: bool = True
    error_message: Optional[str] = None

    # Additional metadata
    streaming: bool = False
    batch_size: int = 1
    timestamp: float = 0.0

    def __post_init__(self):
        """Calculate derived metrics."""
        if self.total_duration_sec > 0:
            if self.total_tokens > 0:
                self.tokens_per_second = self.total_tokens / self.total_duration_sec
                self.latency_per_token_ms = (self.total_duration_sec / self.total_tokens) * 1000

            if self.output_tokens > 0:
                self.tokens_per_second_output_only = self.output_tokens / self.total_duration_sec

        if self.timestamp == 0.0:
            self.timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class TokenGenerationBenchmark:
    """
    Main benchmarking class for token generation speed testing.

    Usage:
        benchmark = TokenGenerationBenchmark()
        results = benchmark.run_all_tests()
        benchmark.save_results("token_speed_report.json")
        benchmark.print_summary()
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("tests/performance/results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: list[TokenGenMetrics] = []

        # Test prompts of varying lengths
        self.test_prompts = {
            "short": "Hello, how are you?",
            "medium": "Explain the concept of technical debt in software development and provide examples.",
            "long": (
                "Please provide a comprehensive analysis of microservices architecture, "
                "including its advantages, disadvantages, common patterns, best practices, "
                "and real-world use cases. Also discuss how it compares to monolithic "
                "architecture and when each approach is more appropriate."
            ),
            "code_generation": (
                "Write a Python function that implements a binary search tree with insert, "
                "delete, search, and in-order traversal methods. Include comprehensive "
                "docstrings and type hints."
            ),
        }

    async def measure_agent_generation_speed(
        self,
        agent: BaseAgent,
        prompt: str,
        test_name: str = "agent_test",
        max_tokens: int = 500,
    ) -> TokenGenMetrics:
        """
        Measure token generation speed for a single agent.

        Args:
            agent: The agent to test
            prompt: Input prompt
            test_name: Name for this test
            max_tokens: Maximum tokens to generate

        Returns:
            TokenGenMetrics with performance data
        """
        start_time = time.perf_counter()
        ttft = None
        output_text = ""

        try:
            # Call agent (this will vary based on your agent implementation)
            # Adjust this based on your actual agent API
            if hasattr(agent, "run_async"):
                output_text = await agent.run_async(prompt)
            elif hasattr(agent, "improve_content"):
                output_text = await agent.improve_content(prompt)
            elif hasattr(agent, "chat"):
                output_text = await agent.chat(prompt)
            else:
                raise AttributeError("Agent doesn't have expected methods")

            duration = time.perf_counter() - start_time

            # Count tokens
            input_tokens = estimate_token_count(prompt)
            output_tokens = estimate_token_count(output_text)

            return TokenGenMetrics(
                test_name=test_name,
                backend=getattr(agent, 'backend', 'unknown'),
                model_name=getattr(agent, 'model', 'unknown'),
                total_duration_sec=duration,
                total_tokens=input_tokens + output_tokens,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                streaming=False,
            )

        except Exception as e:
            duration = time.perf_counter() - start_time
            return TokenGenMetrics(
                test_name=test_name,
                backend="unknown",
                model_name="unknown",
                total_duration_sec=duration,
                success=False,
                error_message=str(e),
            )

    async def measure_streaming_speed(
        self,
        prompt: str,
        test_name: str = "streaming_test",
        config: Optional[StreamingConfig] = None,
    ) -> TokenGenMetrics:
        """
        Measure token generation speed with streaming enabled.

        Args:
            prompt: Input prompt
            test_name: Name for this test
            config: Streaming configuration

        Returns:
            TokenGenMetrics with streaming performance data
        """
        if not HAS_PYAGENT:
            pytest.skip("PyAgent not available")

        start_time = time.perf_counter()
        ttft = None
        tokens_received = 0

        try:
            engine = StreamingVllmEngine(config)

            if not engine.is_available:
                pytest.skip("vLLM not available")

            stream_iter = TokenStreamIterator()

            async for token in engine.generate_stream(prompt):
                if ttft is None:
                    ttft = time.perf_counter() - start_time
                tokens_received += 1

            duration = time.perf_counter() - start_time

            # Get metrics from iterator
            tps = stream_iter.tokens_per_second or 0.0

            input_tokens = estimate_token_count(prompt)

            return TokenGenMetrics(
                test_name=test_name,
                backend="vllm",
                model_name=config.model if config else "unknown",
                total_duration_sec=duration,
                time_to_first_token_sec=ttft,
                total_tokens=input_tokens + tokens_received,
                input_tokens=input_tokens,
                output_tokens=tokens_received,
                streaming=True,
            )

        except Exception as e:
            duration = time.perf_counter() - start_time
            return TokenGenMetrics(
                test_name=test_name,
                backend="vllm",
                model_name="unknown",
                total_duration_sec=duration,
                success=False,
                error_message=str(e),
                streaming=True,
            )

    async def measure_batch_generation_speed(
        self,
        agent: BaseAgent,
        prompts: list[str],
        test_name: str = "batch_test",
    ) -> TokenGenMetrics:
        """
        Measure token generation speed for batch processing.

        Args:
            agent: The agent to test
            prompts: List of prompts to process
            test_name: Name for this test

        Returns:
            Aggregated TokenGenMetrics for the batch
        """
        start_time = time.perf_counter()
        total_input = 0
        total_output = 0

        try:
            for prompt in prompts:
                if hasattr(agent, "run_async"):
                    output = await agent.run_async(prompt)
                elif hasattr(agent, "improve_content"):
                    output = await agent.improve_content(prompt)
                elif hasattr(agent, "chat"):
                    output = await agent.chat(prompt)
                else:
                    raise AttributeError("Agent doesn't have expected methods")

                total_input += estimate_token_count(prompt)
                total_output += estimate_token_count(output)

            duration = time.perf_counter() - start_time

            return TokenGenMetrics(
                test_name=test_name,
                backend=getattr(agent, 'backend', 'unknown'),
                model_name=getattr(agent, 'model', 'unknown'),
                total_duration_sec=duration,
                total_tokens=total_input + total_output,
                input_tokens=total_input,
                output_tokens=total_output,
                batch_size=len(prompts),
            )

        except Exception as e:
            duration = time.perf_counter() - start_time
            return TokenGenMetrics(
                test_name=test_name,
                backend="unknown",
                model_name="unknown",
                total_duration_sec=duration,
                batch_size=len(prompts),
                success=False,
                error_message=str(e),
            )

    async def run_single_prompt_tests(self, agent: BaseAgent) -> list[TokenGenMetrics]:
        """Run tests with different prompt lengths."""
        results = []

        for prompt_type, prompt in self.test_prompts.items():
            print(f"\n🔄 Testing {prompt_type} prompt...")
            metric = await self.measure_agent_generation_speed(
                agent=agent,
                prompt=prompt,
                test_name=f"single_{prompt_type}",
            )
            results.append(metric)
            self._print_metric(metric)

        self.results.extend(results)
        return results

    async def run_streaming_tests(self) -> list[TokenGenMetrics]:
        """Run streaming performance tests."""
        results = []

        for prompt_type, prompt in self.test_prompts.items():
            print(f"\n🌊 Testing streaming with {prompt_type} prompt...")

            try:
                metric = await self.measure_streaming_speed(
                    prompt=prompt,
                    test_name=f"streaming_{prompt_type}",
                )
                results.append(metric)
                self._print_metric(metric)
            except Exception as e:
                print(f"❌ Streaming test failed: {e}")

        self.results.extend(results)
        return results

    async def run_batch_tests(
        self, agent: BaseAgent, batch_sizes: list[int] | None = None
    ) -> list[TokenGenMetrics]:
        """Run batch processing tests."""
        if batch_sizes is None:
            batch_sizes = [5, 10, 20]
        results = []

        for batch_size in batch_sizes:
            print(f"\n📦 Testing batch size {batch_size}...")

            # Use short prompts for batching
            prompts = [self.test_prompts["short"]] * batch_size

            metric = await self.measure_batch_generation_speed(
                agent=agent,
                prompts=prompts,
                test_name=f"batch_{batch_size}",
            )
            results.append(metric)
            self._print_metric(metric)

        self.results.extend(results)
        return results

        return results

    async def run_all_tests(
        self,
        agent: Optional[BaseAgent] = None,
        include_streaming: bool = True,
        include_batch: bool = True,
    ) -> list[TokenGenMetrics]:
        """
        Run all token generation tests.

        Args:
            agent: Agent to test (creates BenchmarkAgent if None)
            include_streaming: Whether to include streaming tests
            include_batch: Whether to include batch tests

        Returns:
            List of all test results
        """
        if agent is None:
            # Create a test agent
            if not HAS_PYAGENT:
                pytest.skip("PyAgent not available")
            agent = BenchmarkAgent(".")

        self.results = []  # Clear previous results

        print("=" * 70)
        print("🚀 PyAgent Token Generation Speed Benchmark Suite")
        print("=" * 70)

        # Single prompt tests
        print("\n📝 Running single prompt tests...")
        results = await self.run_single_prompt_tests(agent)

        # Streaming tests
        if include_streaming:
            print("\n🌊 Running streaming tests...")
            results.extend(await self.run_streaming_tests())

        # Batch tests
        if include_batch:
            print("\n📦 Running batch tests...")
            results.extend(await self.run_batch_tests(agent))

        self.results = results
        return results

    def _print_metric(self, metric: TokenGenMetrics):
        """Print a single metric in a formatted way."""
        status = "✅" if metric.success else "❌"
        print(f"{status} {metric.test_name}")

        if metric.success:
            print(f"   Model: {metric.model_name}")
            print(f"   Tokens/sec: {metric.tokens_per_second:.2f}")
            print(f"   Output tokens/sec: {metric.tokens_per_second_output_only:.2f}")
            print(f"   Latency/token: {metric.latency_per_token_ms:.2f}ms")
            print(f"   Total tokens: {metric.total_tokens} (in: {metric.input_tokens}, out: {metric.output_tokens})")
            print(f"   Duration: {metric.total_duration_sec:.3f}s")

            if metric.time_to_first_token_sec is not None:
                print(f"   TTFT: {metric.time_to_first_token_sec:.3f}s")
        else:
            print(f"   Error: {metric.error_message}")

    def print_summary(self):
        """Print a summary table of all results."""
        if not self.results:
            print("No results to display.")
            return

        print("\n" + "=" * 70)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 70)

        successful = [r for r in self.results if r.success]

        if not successful:
            print("❌ No successful tests.")
            return

        # Overall stats
        avg_tps = statistics.mean([r.tokens_per_second for r in successful])
        avg_tps_output = statistics.mean([r.tokens_per_second_output_only for r in successful])
        avg_latency = statistics.mean([r.latency_per_token_ms for r in successful])

        print(f"\n🎯 Average Performance:")
        print(f"   Tokens/sec (total): {avg_tps:.2f}")
        print(f"   Tokens/sec (output only): {avg_tps_output:.2f}")
        print(f"   Latency/token: {avg_latency:.2f}ms")

        # Best performance
        best_tps = max(successful, key=lambda r: r.tokens_per_second)
        print(f"\n🏆 Best Performance:")
        print(f"   Test: {best_tps.test_name}")
        print(f"   Model: {best_tps.model_name}")
        print(f"   Tokens/sec: {best_tps.tokens_per_second:.2f}")

        # Group by backend
        by_backend: dict[str, list[TokenGenMetrics]] = {}
        for r in successful:
            by_backend.setdefault(r.backend, []).append(r)

        print(f"\n📊 Performance by Backend:")
        for backend, metrics in by_backend.items():
            avg = statistics.mean([m.tokens_per_second for m in metrics])
            print(f"   {backend}: {avg:.2f} tokens/sec (n={len(metrics)})")

        # Failures
        failures = [r for r in self.results if not r.success]
        if failures:
            print(f"\n⚠️  Failed Tests: {len(failures)}")
            for f in failures:
                print(f"   - {f.test_name}: {f.error_message}")

    def save_results(self, filename: str = "token_generation_benchmark.json"):
        """Save results to JSON file."""
        output_path = self.output_dir / filename

        results_dict = {
            "timestamp": time.time(),
            "total_tests": len(self.results),
            "successful_tests": sum(1 for r in self.results if r.success),
            "failed_tests": sum(1 for r in self.results if not r.success),
            "results": [r.to_dict() for r in self.results],
        }

        with open(output_path, "w") as f:
            json.dump(results_dict, f, indent=2)

        print(f"\n💾 Results saved to: {output_path}")
        return output_path

    def compare_with_baseline(self, baseline_file: Path) -> dict[str, Any]:
        """
        Compare current results with a baseline.

        Args:
            baseline_file: Path to baseline JSON file

        Returns:
            Comparison statistics
        """
        if not baseline_file.exists():
            print(f"⚠️  Baseline file not found: {baseline_file}")
            return {}

        with open(baseline_file) as f:
            baseline_data = json.load(f)

        baseline_results = [TokenGenMetrics(**r) for r in baseline_data.get("results", [])]
        baseline_successful = [r for r in baseline_results if r.success]
        current_successful = [r for r in self.results if r.success]

        if not baseline_successful or not current_successful:
            return {}

        baseline_avg_tps = statistics.mean([r.tokens_per_second for r in baseline_successful])
        current_avg_tps = statistics.mean([r.tokens_per_second for r in current_successful])

        improvement = ((current_avg_tps - baseline_avg_tps) / baseline_avg_tps) * 100

        comparison = {
            "baseline_avg_tps": baseline_avg_tps,
            "current_avg_tps": current_avg_tps,
            "improvement_percent": improvement,
            "regression": improvement < -5,  # More than 5% slower
        }

        print(f"\n📈 Baseline Comparison:")
        print(f"   Baseline: {baseline_avg_tps:.2f} tokens/sec")
        print(f"   Current:  {current_avg_tps:.2f} tokens/sec")
        print(f"   Change:   {improvement:+.1f}%")

        if comparison["regression"]:
            print("   ⚠️  PERFORMANCE REGRESSION DETECTED!")
        elif improvement > 5:
            print("   🎉 Performance improved!")

        return comparison


# ============================================================================
# PYTEST TEST CASES
# ============================================================================

@pytest.fixture
def benchmark(tmp_path):
    """Create benchmark instance for tests."""
    return TokenGenerationBenchmark(output_dir=tmp_path)


@pytest.fixture
def test_agent():
    """Create test agent if PyAgent is available."""
    if not HAS_PYAGENT:
        pytest.skip("PyAgent not available")
    return BenchmarkAgent(".")


@pytest.mark.asyncio
async def test_single_prompt_short(benchmark, test_agent):
    """Test token generation with a short prompt."""
    metric = await benchmark.measure_agent_generation_speed(
        agent=test_agent,
        prompt=benchmark.test_prompts["short"],
        test_name="test_short",
    )

    assert metric.total_duration_sec > 0
    if metric.success:
        assert metric.tokens_per_second > 0
        assert metric.total_tokens > 0


@pytest.mark.asyncio
async def test_single_prompt_medium(benchmark, test_agent):
    """Test token generation with a medium prompt."""
    metric = await benchmark.measure_agent_generation_speed(
        agent=test_agent,
        prompt=benchmark.test_prompts["medium"],
        test_name="test_medium",
    )

    assert metric.total_duration_sec > 0
    if metric.success:
        assert metric.tokens_per_second > 0
        short_tokens = estimate_token_count(benchmark.test_prompts["short"])
        assert metric.input_tokens > short_tokens


@pytest.mark.asyncio
async def test_batch_generation(benchmark, test_agent):
    """Test batch token generation."""
    prompts = [benchmark.test_prompts["short"]] * 5

    metric = await benchmark.measure_batch_generation_speed(
        agent=test_agent,
        prompts=prompts,
        test_name="test_batch_5",
    )

    assert metric.batch_size == 5
    assert metric.total_duration_sec > 0


@pytest.mark.asyncio
async def test_streaming_generation(benchmark):
    """Test streaming token generation."""
    metric = await benchmark.measure_streaming_speed(
        prompt=benchmark.test_prompts["short"],
        test_name="test_streaming",
    )

    assert metric.streaming is True
    assert metric.total_duration_sec > 0


def test_token_estimation_rust():
    """Test Rust-accelerated token estimation if available."""
    if not HAS_RUST:
        pytest.skip("Rust core not available")

    text = "Hello, world! This is a test."
    count = rust_core.estimate_tokens_rust(text)

    assert count > 0
    assert isinstance(count, int)


@pytest.mark.asyncio
async def test_full_benchmark_suite(benchmark, test_agent):
    """Run the complete benchmark suite."""
    results = await benchmark.run_all_tests(
        agent=test_agent,
        include_streaming=False,  # Skip streaming in pytest by default
        include_batch=True,
    )

    assert len(results) > 0
    assert any(r.success for r in results)

    # Print summary
    benchmark.print_summary()


@pytest.mark.asyncio
async def test_save_and_load_results(benchmark, test_agent, tmp_path):
    """Test saving and loading benchmark results."""
    await benchmark.run_single_prompt_tests(test_agent)

    output_file = tmp_path / "test_results.json"
    saved_path = benchmark.save_results(str(output_file.name))

    assert saved_path.exists()

    # Load and verify
    with open(saved_path) as f:
        data = json.load(f)

    assert "results" in data
    assert len(data["results"]) > 0


# ============================================================================
# MAIN ENTRY POINT FOR STANDALONE EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Run the benchmark suite standalone.

    Usage:
        python test_token_generation_speed.py
    """
    import sys

    print("🚀 PyAgent Token Generation Speed Benchmark")
    print("=" * 70)

    # Create benchmark
    benchmark = TokenGenerationBenchmark()

    # Create test agent
    try:
        if HAS_PYAGENT:
            agent = BenchmarkAgent(".")
        else:
            print("❌ PyAgent not available. Cannot run benchmarks.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        sys.exit(1)

    # Run all tests
    try:
        results = asyncio.run(benchmark.run_all_tests(
            agent=agent,
            include_streaming=True,
            include_batch=True,
        ))

        # Print summary
        benchmark.print_summary()

        # Save results
        output_file = benchmark.save_results()

        print("\n✅ Benchmark complete!")
        print(f"📊 Total tests: {len(results)}")
        print(f"✅ Successful: {sum(1 for r in results if r.success)}")
        print(f"❌ Failed: {sum(1 for r in results if not r.success)}")

    except KeyboardInterrupt:
        print("\n⚠️  Benchmark interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
