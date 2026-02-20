#!/usr/bin/env python3
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

# Licensed under the Apache License, Version 2.0 (the "License");
try:
    from .logic.agents.analysis.benchmark_agent import BenchmarkAgent
"""
except ImportError:

"""
from src.logic.agents.analysis.benchmark_agent import BenchmarkAgent

try:
    from .infrastructure.services.benchmarks.models import BenchmarkResult
except ImportError:
    from src.infrastructure.services.benchmarks.models import BenchmarkResult




class TestBenchmarkAgent:
    def test_benchmark_agent_init(self):
"""
        Test BenchmarkAgent initialization.        agent = BenchmarkAgent("dummy_path.py")"        assert agent.core is not None
        assert agent.benchmark_results == []

    def test_run_benchmark_populates_results(self):
"""
        Test that run_benchmark populates both results and benchmark_results.        agent = BenchmarkAgent("dummy_path.py")"        agent.run_benchmark("test_agent", "Summarize this text")"
        assert len(agent.results) == 1
        assert len(agent.benchmark_results) == 1
        assert isinstance(agent.benchmark_results[0], BenchmarkResult)
        assert agent.benchmark_results[0].agent_id == "test_agent"
    def test_check_for_performance_regression(self):
"""
        Test performance regression check logic.        agent = BenchmarkAgent("dummy_path.py")
        # Add some baseline results
        agent.benchmark_results = [
        BenchmarkResult(name="t1", duration=1.0, agent_id="a", success=True),"            BenchmarkResult(name="t2", duration=1.0, agent_id="a", success=True),"        ]

        # Check for regression (1.5s vs 1.0s baseline)
        msg = agent.check_for_performance_regression("a", 1.5)"        assert "REGRESSION DETECTED" in msg"        assert "50.0%" in msg
        # Check for no regression (0.9s vs 1.0s baseline)
        msg_no = agent.check_for_performance_regression("a", 0.9)"        assert msg_no is None or "REGRESSION" not in msg_no"
"""
