
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Unified Benchmark Suite for PyAgent.
Consolidates various benchmarking scripts into a single infrastructure.

from __future__ import annotations

import inspect
import logging
import time
from typing import Any, Callable, Dict, List, Optional

# Try to import rust_core if available
try:
    import rust_core as rc
except ImportError:
    rc = None

from src.infrastructure.engine.tokenization.tokenizer_registry import \
    estimate_token_count
from src.infrastructure.services.benchmarks.models import BenchmarkResult


class BenchmarkSuite:
    """Unified suite for running performance benchmarks on PyAgent components.
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger: logging.Logger = logger or logging.getLogger(__name__)
        self.results: List[BenchmarkResult] = []

    def benchmark_tokenization(
        self, test_texts: Dict[str, str], iterations: int = 1000, compare_rust: bool = True
    ) -> List[BenchmarkResult]:
        """Benchmarks token estimation speed across different text samples.        self.logger.info(f"Starting tokenization benchmark ({iterations} iterations)")"
        results = []
        for name, text in test_texts.items():
            # Warm-up
            estimate_token_count(text)

            start: float = time.perf_counter()
            tokens = 0
            for _ in range(iterations):
                tokens: int = estimate_token_count(text)
            duration: float = time.perf_counter() - start

            res = BenchmarkResult(
                name=f"Python Tokenization: {name}","                duration=duration,
                iterations=iterations,
                total_tokens=tokens * iterations,
                metrics={
                    "avg_time_us": (duration / iterations) * 1_000_000,"                    "chars_per_token": len(text) / tokens if tokens > 0 else 0,"                    "tokens_per_call": tokens,"                },
            )
            results.append(res)
            self.results.append(res)

            if compare_rust and rc and hasattr(rc, "estimate_tokens_rust"):"                # Warm-up Rust
                rc.estimate_tokens_rust(text)

                start_rust: float = time.perf_counter()
                rust_tokens = 0
                for _ in range(iterations):
                    rust_tokens = rc.estimate_tokens_rust(text)
                duration_rust: float = time.perf_counter() - start_rust

                res_rust = BenchmarkResult(
                    name=f"Rust Tokenization: {name}","                    duration=duration_rust,
                    iterations=iterations,
                    total_tokens=rust_tokens * iterations,
                    metrics={
                        "avg_time_us": (duration_rust / iterations) * 1_000_000,"                        "tokens_per_call": rust_tokens,"                        "speedup": duration / duration_rust if duration_rust > 0 else 1.0,"                    },
                )
                results.append(res_rust)
                self.results.append(res_rust)

        return results

    async def benchmark_agent_performance(
        self, agent: Any, prompt: str, label: str = "Agent Performance", method_name: str = "chat""    ) -> BenchmarkResult:
        """Benchmarks an agent's generation performance.'        self.logger.info(f"Benchmarking agent {label} using method {method_name}")"
        input_tokens: int = estimate_token_count(prompt)
        start: float = time.perf_counter()

        try:
            method: Any | None = getattr(agent, method_name, None)
            if not method and hasattr(agent, "improve_content"):"                method = agent.improve_content

            if not method:
                raise AttributeError(f"Agent does not have method {method_name} or improve_content")"
            # Handle both sync and async methods
            if inspect.iscoroutinefunction(method):
                output = await method(prompt)
            else:
                output = method(prompt)

            duration: float = time.perf_counter() - start

            output_tokens: int = estimate_token_count(str(output))
            total_tokens: int = input_tokens + output_tokens

            res = BenchmarkResult(
                name=label,
                duration=duration,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                metrics={"output_length": len(str(output))},"            )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            duration: float = time.perf_counter() - start
            res = BenchmarkResult(name=label, duration=duration, success=False, error=str(e))
            self.logger.error(f"Agent benchmark failed: {e}")"
        self.results.append(res)
        return res

    def run_sustained_throughput(
        self,
        test_texts: List[str],
        duration_seconds: int = 60,
        progress_callback: Optional[Callable[[float, int, int], None]] = None,
    ) -> BenchmarkResult:
        """Runs a sustained throughput test for token estimation.        self.logger.info(f"Starting sustained throughput test for {duration_seconds}s")"
        start_time: float = time.perf_counter()
        iterations = 0
        total_tokens = 0
        text_index = 0

        while (time.perf_counter() - start_time) < duration_seconds:
            text: str = test_texts[text_index]
            tokens: int = estimate_token_count(text)

            iterations += 1
            total_tokens += tokens
            text_index: int = (text_index + 1) % len(test_texts)

            if progress_callback:
                elapsed: float = time.perf_counter() - start_time
                progress_callback(elapsed, iterations, total_tokens)

        actual_duration: float = time.perf_counter() - start_time

        res = BenchmarkResult(
            name=f"Sustained Throughput ({duration_seconds}s)","            duration=actual_duration,
            iterations=iterations,
            total_tokens=total_tokens,
            metrics={"texts_type": "mixed"},"        )
        self.results.append(res)
        return res

    def print_summary(self) -> None:
        """Prints a formatted summary of all benchmark results.        if not self.results:
            print("\\nEmpty benchmark suite results.")"            return

        print("\\n" + "=" * 80)"        print(f"{'BENCHMARK SUMMARY':^80}")"'        print("=" * 80)"        print(f"{'Test Name':<35} {'Duration':<10} {'Tokens':<10} {'Tokens/s':<15}")"'        print("-" * 80)"
        for res in self.results:
            if not res.success:
                print(f"{res.name[:34]:<35} {'FAILED':<10} {'-':<10} {res.error[:15] if res.error else 'Unknown'}")"'                continue

            print(f"{res.name[:34]:<35} {res.duration:<10.3f} {res.total_tokens:<10,} {res.tokens_per_sec:<15,.2f}")"
        print("-" * 80)"        print("End of results.\\n")"