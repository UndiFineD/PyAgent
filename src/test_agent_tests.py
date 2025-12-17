#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for agent-tests.py."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def tests_module() -> Any:
    """Load the tests agent module."""
    with agent_dir_on_path():
        return load_agent_module("agent-tests.py")


@pytest.fixture()
def agent(tests_module: Any, tmp_path: Path) -> Any:
    """Create agent for testing."""
    target = tmp_path / "test_something.py"
    target.write_text("# Tests\n", encoding="utf-8")
    return tests_module.TestsAgent(str(target))


def test_tests_agent_update_file_writes_raw(tmp_path: Path) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-tests.py")
    target = tmp_path / "test_something.py"
    agent = mod.TestsAgent(str(target))
    agent.current_content = "print('hi')\n"
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "print('hi')\n"


# ========== TestPriority Tests ==========

class TestTestPriority:
    """Tests for TestPriority enum."""

    def test_priority_values(self, tests_module: Any) -> None:
        """Test that priority values are correct."""
        assert tests_module.TestPriority.CRITICAL.value == 5
        assert tests_module.TestPriority.HIGH.value == 4
        assert tests_module.TestPriority.MEDIUM.value == 3
        assert tests_module.TestPriority.LOW.value == 2
        assert tests_module.TestPriority.SKIP.value == 1

    def test_all_priorities_exist(self, tests_module: Any) -> None:
        """Test all priority levels exist."""
        priorities = list(tests_module.TestPriority)
        assert len(priorities) == 5


# ========== TestStatus Tests ==========

class TestTestStatus:
    """Tests for TestStatus enum."""

    def test_status_values(self, tests_module: Any) -> None:
        """Test that status values are correct strings."""
        assert tests_module.TestStatus.PASSED.value == "passed"
        assert tests_module.TestStatus.FAILED.value == "failed"
        assert tests_module.TestStatus.FLAKY.value == "flaky"

    def test_all_statuses_exist(self, tests_module: Any) -> None:
        """Test all statuses exist."""
        statuses = list(tests_module.TestStatus)
        assert len(statuses) == 5


# ========== TestCase Tests ==========

class TestTestCase:
    """Tests for TestCase dataclass."""

    def test_create_test_case(self, tests_module: Any) -> None:
        """Test creating a test case."""
        test = tests_module.TestCase(
            id="test123",
            name="test_something",
            file_path="test.py",
            line_number=10
        )
        assert test.id == "test123"
        assert test.name == "test_something"
        assert test.priority == tests_module.TestPriority.MEDIUM
        assert test.status == tests_module.TestStatus.PASSED


# ========== Add Test Tests ==========

class TestAddTest:
    """Tests for adding tests."""

    def test_add_simple_test(self, agent: Any, tests_module: Any) -> None:
        """Test adding a simple test."""
        test = agent.add_test(
            name="test_function",
            file_path="test.py",
            line_number=10
        )
        assert test.id is not None
        assert len(agent.get_tests()) == 1

    def test_add_test_with_priority(self, agent: Any, tests_module: Any) -> None:
        """Test adding test with custom priority."""
        test = agent.add_test(
            name="test_critical",
            file_path="test.py",
            line_number=5,
            priority=tests_module.TestPriority.CRITICAL
        )
        assert test.priority == tests_module.TestPriority.CRITICAL

    def test_add_test_with_tags(self, agent: Any) -> None:
        """Test adding test with tags."""
        test = agent.add_test(
            name="test_tagged",
            file_path="test.py",
            line_number=15,
            tags=["slow", "integration"]
        )
        assert "slow" in test.tags
        assert "integration" in test.tags


# ========== Test Retrieval Tests ==========

class TestTestRetrieval:
    """Tests for test retrieval methods."""

    def test_get_all_tests(self, agent: Any, tests_module: Any) -> None:
        """Test getting all tests."""
        agent.add_test("test1", "a.py", 10, tests_module.TestPriority.HIGH)
        agent.add_test("test2", "b.py", 20, tests_module.TestPriority.LOW)
        tests = agent.get_tests()
        assert len(tests) == 2

    def test_get_test_by_id(self, agent: Any) -> None:
        """Test getting test by ID."""
        test = agent.add_test("test_find", "test.py", 10)
        found = agent.get_test_by_id(test.id)
        assert found is not None
        assert found.id == test.id

    def test_get_test_by_name(self, agent: Any) -> None:
        """Test getting test by name."""
        agent.add_test("test_specific", "test.py", 10)
        found = agent.get_test_by_name("test_specific")
        assert found is not None
        assert found.name == "test_specific"

    def test_get_tests_by_priority(self, agent: Any, tests_module: Any) -> None:
        """Test filtering by priority."""
        agent.add_test("high1", "a.py", 10, tests_module.TestPriority.HIGH)
        agent.add_test("high2", "b.py", 20, tests_module.TestPriority.HIGH)
        agent.add_test("low", "c.py", 30, tests_module.TestPriority.LOW)
        high = agent.get_tests_by_priority(tests_module.TestPriority.HIGH)
        assert len(high) == 2

    def test_get_tests_by_tag(self, agent: Any) -> None:
        """Test filtering by tag."""
        agent.add_test("tagged1", "a.py", 10, tags=["slow"])
        agent.add_test("tagged2", "b.py", 20, tags=["slow", "unit"])
        agent.add_test("untagged", "c.py", 30)
        slow = agent.get_tests_by_tag("slow")
        assert len(slow) == 2


# ========== Test Prioritization Tests ==========

class TestTestPrioritization:
    """Tests for test prioritization."""

    def test_prioritize_tests(self, agent: Any, tests_module: Any) -> None:
        """Test prioritizing tests."""
        agent.add_test("low", "a.py", 10, tests_module.TestPriority.LOW)
        agent.add_test("critical", "b.py", 20, tests_module.TestPriority.CRITICAL)
        agent.add_test("medium", "c.py", 30, tests_module.TestPriority.MEDIUM)
        prioritized = agent.prioritize_tests()
        assert prioritized[0].priority == tests_module.TestPriority.CRITICAL

    def test_calculate_priority_score(self, agent: Any, tests_module: Any) -> None:
        """Test priority score calculation."""
        test = agent.add_test("test", "test.py", 10, tests_module.TestPriority.CRITICAL)
        score = agent.calculate_priority_score(test)
        assert score > 0
        assert score <= 100


# ========== Flakiness Detection Tests ==========

class TestFlakinessDetection:
    """Tests for flakiness detection."""

    def test_calculate_flakiness(self, agent: Any) -> None:
        """Test flakiness calculation."""
        test = agent.add_test("test_flaky", "test.py", 10)
        test.run_count = 10
        test.failure_count = 3
        flakiness = agent.calculate_flakiness(test)
        assert flakiness == 0.3

    def test_detect_flaky_tests(self, agent: Any, tests_module: Any) -> None:
        """Test detecting flaky tests."""
        test = agent.add_test("test_flaky", "test.py", 10)
        test.run_count = 10
        test.failure_count = 5  # 50% failure rate
        flaky = agent.detect_flaky_tests()
        assert len(flaky) == 1
        assert flaky[0].status == tests_module.TestStatus.FLAKY

    def test_set_flakiness_threshold(self, agent: Any) -> None:
        """Test setting flakiness threshold."""
        agent.set_flakiness_threshold(0.2)
        assert agent._flakiness_threshold == 0.2

    def test_quarantine_flaky_test(self, agent: Any, tests_module: Any) -> None:
        """Test quarantining a flaky test."""
        test = agent.add_test("test_quarantine", "test.py", 10)
        result = agent.quarantine_flaky_test(test.id)
        assert result is True
        assert test.priority == tests_module.TestPriority.SKIP
        assert "quarantined" in test.tags


# ========== Coverage Gap Tests ==========

class TestCoverageGaps:
    """Tests for coverage gap analysis."""

    def test_add_coverage_gap(self, agent: Any, tests_module: Any) -> None:
        """Test adding coverage gap."""
        gap = agent.add_coverage_gap(
            file_path="source.py",
            line_start=10,
            line_end=20,
            coverage_type=tests_module.CoverageType.LINE
        )
        assert gap.file_path == "source.py"
        assert len(agent.get_coverage_gaps()) == 1

    def test_get_coverage_gaps_by_file(self, agent: Any, tests_module: Any) -> None:
        """Test getting coverage gaps by file."""
        agent.add_coverage_gap("a.py", 10, 20)
        agent.add_coverage_gap("a.py", 30, 40)
        agent.add_coverage_gap("b.py", 10, 20)
        gaps = agent.get_coverage_gaps_by_file("a.py")
        assert len(gaps) == 2

    def test_suggest_tests_for_gap(self, agent: Any, tests_module: Any) -> None:
        """Test generating test suggestions for gap."""
        gap = agent.add_coverage_gap("source.py", 10, 20)
        suggestion = agent.suggest_tests_for_gap(gap)
        assert "def test_" in suggestion
        assert "source.py" in suggestion


# ========== Test Data Factory Tests ==========

class TestTestDataFactories:
    """Tests for test data factories."""

    def test_add_factory(self, agent: Any) -> None:
        """Test adding a factory."""
        factory = agent.add_factory(
            name="create_user",
            return_type="User",
            parameters={"name": "str", "age": "int"}
        )
        assert factory.name == "create_user"
        assert factory.return_type == "User"

    def test_get_factory(self, agent: Any) -> None:
        """Test getting a factory."""
        agent.add_factory("create_item", "Item")
        factory = agent.get_factory("create_item")
        assert factory is not None
        assert factory.name == "create_item"

    def test_generate_factory_code(self, agent: Any) -> None:
        """Test generating factory code."""
        factory = agent.add_factory(
            name="create_data",
            return_type="Data",
            parameters={"x": "int"},
            generator="return Data(x=x)"
        )
        code = agent.generate_factory_code(factory)
        assert "def create_data" in code
        assert "-> Data" in code


# ========== Test Run Recording Tests ==========

class TestTestRunRecording:
    """Tests for test run recording."""

    def test_record_test_run(self, agent: Any, tests_module: Any) -> None:
        """Test recording a test run."""
        agent.add_test("test1", "test.py", 10)
        agent.add_test("test2", "test.py", 20)

        results = {
            "test1": tests_module.TestStatus.PASSED,
            "test2": tests_module.TestStatus.FAILED
        }
        run = agent.record_test_run(results, duration_ms=1000)

        assert run.total_tests == 2
        assert run.passed == 1
        assert run.failed == 1

    def test_get_latest_run(self, agent: Any, tests_module: Any) -> None:
        """Test getting latest run."""
        results = {"test1": tests_module.TestStatus.PASSED}
        agent.record_test_run(results)
        latest = agent.get_latest_run()
        assert latest is not None


# ========== Parallel Execution Tests ==========

class TestParallelExecution:
    """Tests for parallel execution."""

    def test_enable_parallel(self, agent: Any) -> None:
        """Test enabling parallel execution."""
        agent.enable_parallel(8)
        assert agent.is_parallel_enabled() is True
        assert agent._max_parallel == 8

    def test_disable_parallel(self, agent: Any) -> None:
        """Test disabling parallel execution."""
        agent.enable_parallel()
        agent.disable_parallel()
        assert agent.is_parallel_enabled() is False

    def test_get_parallel_groups(self, agent: Any, tests_module: Any) -> None:
        """Test grouping tests for parallel execution."""
        agent.add_test("test1", "a.py", 10)
        agent.add_test("test2", "b.py", 20)
        agent.enable_parallel(2)
        groups = agent.get_parallel_groups()
        assert len(groups) >= 1


# ========== Documentation Tests ==========

class TestDocumentationGeneration:
    """Tests for documentation generation."""

    def test_generate_test_documentation(self, agent: Any, tests_module: Any) -> None:
        """Test documentation generation."""
        agent.add_test("test_critical", "a.py", 10, tests_module.TestPriority.CRITICAL)
        agent.add_test("test_low", "b.py", 20, tests_module.TestPriority.LOW)
        docs = agent.generate_test_documentation()
        assert "# Test Documentation" in docs
        assert "Total Tests" in docs


# ========== Export Tests ==========

class TestExport:
    """Tests for test export."""

    def test_export_json(self, agent: Any) -> None:
        """Test JSON export."""
        agent.add_test("test1", "a.py", 10)
        agent.add_test("test2", "b.py", 20)
        exported = agent.export_tests("json")
        data = json.loads(exported)
        assert len(data) == 2


# ========== Statistics Tests ==========

class TestStatistics:
    """Tests for test statistics."""

    def test_calculate_statistics(self, agent: Any, tests_module: Any) -> None:
        """Test statistics calculation."""
        agent.add_test("test1", "a.py", 10, tests_module.TestPriority.HIGH)
        agent.add_test("test2", "b.py", 20, tests_module.TestPriority.LOW)
        stats = agent.calculate_statistics()
        assert stats["total_tests"] == 2
        assert "by_status" in stats
        assert "by_priority" in stats


# ========== Session 7 Tests: New Enums ==========


class TestSession7Enums:
    """Tests for Session 7 enums."""

    def test_browser_type_enum(self, tests_module: Any) -> None:
        """Test BrowserType enum values."""
        assert tests_module.BrowserType.CHROME.value == "chrome"
        assert tests_module.BrowserType.FIREFOX.value == "firefox"
        assert tests_module.BrowserType.SAFARI.value == "safari"

    def test_test_source_type_enum(self, tests_module: Any) -> None:
        """Test TestSourceType enum values."""
        assert tests_module.TestSourceType.PYTEST.value == "pytest"
        assert tests_module.TestSourceType.JEST.value == "jest"
        assert tests_module.TestSourceType.JUNIT.value == "junit"

    def test_mutation_operator_enum(self, tests_module: Any) -> None:
        """Test MutationOperator enum values."""
        assert tests_module.MutationOperator.ARITHMETIC.value == "arithmetic"
        assert tests_module.MutationOperator.LOGICAL.value == "logical"

    def test_execution_mode_enum(self, tests_module: Any) -> None:
        """Test ExecutionMode enum values."""
        assert tests_module.ExecutionMode.STEP_BY_STEP.value == "step_by_step"
        assert tests_module.ExecutionMode.BREAKPOINT.value == "breakpoint"


# ========== Session 7 Tests: Dataclasses ==========


class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses."""

    def test_visual_regression_config(self, tests_module: Any) -> None:
        """Test VisualRegressionConfig dataclass."""
        config = tests_module.VisualRegressionConfig(baseline_dir="/baselines")
        assert config.diff_threshold == 0.01
        assert tests_module.BrowserType.CHROME in config.browsers

    def test_contract_test(self, tests_module: Any) -> None:
        """Test ContractTest dataclass."""
        contract = tests_module.ContractTest(
            consumer="service-a",
            provider="service-b",
            endpoint="/api / users"
        )
        assert contract.status_code == 200

    def test_test_environment(self, tests_module: Any) -> None:
        """Test TestEnvironment dataclass."""
        env = tests_module.TestEnvironment(name="staging", base_url="http://staging.example.com")
        assert env.variables == {}

    def test_execution_trace(self, tests_module: Any) -> None:
        """Test ExecutionTrace dataclass."""
        trace = tests_module.ExecutionTrace(test_id="test1", timestamp="2025-01-01")
        assert trace.steps == []

    def test_test_dependency(self, tests_module: Any) -> None:
        """Test TestDependency dataclass."""
        dep = tests_module.TestDependency(name="db", dependency_type="Database")
        assert dep.mock_behavior == ""

    def test_cross_browser_config(self, tests_module: Any) -> None:
        """Test CrossBrowserConfig dataclass."""
        config = tests_module.CrossBrowserConfig(
            browsers=[tests_module.BrowserType.CHROME, tests_module.BrowserType.FIREFOX]
        )
        assert config.parallel is True
        assert config.headless is True

    def test_aggregated_result(self, tests_module: Any) -> None:
        """Test AggregatedResult dataclass."""
        result = tests_module.AggregatedResult(
            source=tests_module.TestSourceType.PYTEST,
            test_name="test_example",
            status=tests_module.TestStatus.PASSED,
            duration_ms=100.0,
            timestamp="2025-01-01"
        )
        assert result.metadata == {}

    def test_mutation(self, tests_module: Any) -> None:
        """Test Mutation dataclass."""
        mut = tests_module.Mutation(
            id="mut1",
            file_path="test.py",
            line_number=10,
            operator=tests_module.MutationOperator.ARITHMETIC,
            original_code="a + b",
            mutated_code="a - b"
        )
        assert mut.killed is False

    def test_generated_test(self, tests_module: Any) -> None:
        """Test GeneratedTest dataclass."""
        gen = tests_module.GeneratedTest(
            name="test_func",
            specification="Should return sum",
            generated_code="def test_func(): pass"
        )
        assert gen.validated is False

    def test_test_profile(self, tests_module: Any) -> None:
        """Test TestProfile dataclass."""
        profile = tests_module.TestProfile(
            test_id="test1",
            cpu_time_ms=100.0,
            memory_peak_mb=50.0,
            io_operations=10,
            function_calls=100
        )
        assert profile.timestamp == ""

    def test_schedule_slot(self, tests_module: Any) -> None:
        """Test ScheduleSlot dataclass."""
        slot = tests_module.ScheduleSlot(start_time="10:00", end_time="11:00")
        assert slot.workers == 1


# ========== Session 7 Tests: VisualRegressionTester ==========


class TestVisualRegressionTester:
    """Tests for VisualRegressionTester class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        config = tests_module.VisualRegressionConfig(baseline_dir="/baselines")
        tester = tests_module.VisualRegressionTester(config)
        assert tester.baselines == {}

    def test_capture_baseline(self, tests_module: Any) -> None:
        """Test capturing baseline."""
        config = tests_module.VisualRegressionConfig(baseline_dir="/baselines")
        tester = tests_module.VisualRegressionTester(config)
        image_hash = tester.capture_baseline("button", "/path / to / screenshot.png")
        assert image_hash is not None
        assert "button" in tester.baselines

    def test_compare(self, tests_module: Any) -> None:
        """Test comparison."""
        config = tests_module.VisualRegressionConfig(baseline_dir="/baselines")
        tester = tests_module.VisualRegressionTester(config)
        tester.capture_baseline("button", "/path / to / baseline.png")
        result = tester.compare("button", "/path / to / current.png")
        assert "passed" in result

    def test_generate_diff_report(self, tests_module: Any) -> None:
        """Test diff report generation."""
        config = tests_module.VisualRegressionConfig(baseline_dir="/baselines")
        tester = tests_module.VisualRegressionTester(config)
        report = tester.generate_diff_report()
        assert "Visual Regression Report" in report


# ========== Session 7 Tests: ContractTestRunner ==========


class TestContractTestRunner:
    """Tests for ContractTestRunner class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        runner = tests_module.ContractTestRunner()
        assert runner.contracts == {}

    def test_add_contract(self, tests_module: Any) -> None:
        """Test adding a contract."""
        runner = tests_module.ContractTestRunner()
        contract = runner.add_contract("consumer", "provider", "/api / users")
        assert contract.consumer == "consumer"

    def test_verify_consumer(self, tests_module: Any) -> None:
        """Test consumer verification."""
        runner = tests_module.ContractTestRunner()
        runner.add_contract("consumer", "provider", "/api / users",
                            request_schema={"user_id": "int"})
        result = runner.verify_consumer("consumer:provider:/api / users", {"user_id": 123})
        assert result["valid"] is True

    def test_export_pact(self, tests_module: Any) -> None:
        """Test Pact export."""
        runner = tests_module.ContractTestRunner()
        runner.add_contract("consumer", "provider", "/api / users")
        pact = runner.export_pact("consumer")
        assert "consumer" in pact


# ========== Session 7 Tests: TestSuiteOptimizer ==========


class TestTestSuiteOptimizer:
    """Tests for TestSuiteOptimizer class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        optimizer = tests_module.TestSuiteOptimizer()
        assert optimizer.tests == []

    def test_add_coverage(self, tests_module: Any) -> None:
        """Test adding coverage data."""
        optimizer = tests_module.TestSuiteOptimizer()
        optimizer.add_coverage("test1", {"line1", "line2"})
        assert "test1" in optimizer.coverage_map

    def test_find_redundant_tests(self, tests_module: Any) -> None:
        """Test finding redundant tests."""
        optimizer = tests_module.TestSuiteOptimizer()
        optimizer.add_coverage("test1", {"line1", "line2"})
        optimizer.add_coverage("test2", {"line1", "line2", "line3"})
        redundant = optimizer.find_redundant_tests()
        assert "test1" in redundant

    def test_suggest_removals(self, tests_module: Any) -> None:
        """Test suggesting removals."""
        optimizer = tests_module.TestSuiteOptimizer()
        optimizer.add_coverage("test1", {"line1"})
        optimizer.add_coverage("test2", {"line1", "line2"})
        suggestions = optimizer.suggest_removals()
        assert len(suggestions) >= 1


# ========== Session 7 Tests: EnvironmentProvisioner ==========


class TestEnvironmentProvisioner:
    """Tests for EnvironmentProvisioner class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        provisioner = tests_module.EnvironmentProvisioner()
        assert provisioner.environments == {}

    def test_register_environment(self, tests_module: Any) -> None:
        """Test registering environment."""
        provisioner = tests_module.EnvironmentProvisioner()
        env = provisioner.register_environment("staging", "http://staging.example.com")
        assert env.name == "staging"

    def test_provision(self, tests_module: Any) -> None:
        """Test provisioning."""
        provisioner = tests_module.EnvironmentProvisioner()
        provisioner.register_environment("staging")
        result = provisioner.provision("staging")
        assert result["success"] is True

    def test_teardown(self, tests_module: Any) -> None:
        """Test teardown."""
        provisioner = tests_module.EnvironmentProvisioner()
        provisioner.register_environment("staging")
        provisioner.provision("staging")
        result = provisioner.teardown("staging")
        assert result["success"] is True


# ========== Session 7 Tests: ExecutionReplayer ==========


class TestExecutionReplayer:
    """Tests for ExecutionReplayer class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        replayer = tests_module.ExecutionReplayer()
        assert replayer.traces == {}

    def test_start_recording(self, tests_module: Any) -> None:
        """Test starting recording."""
        replayer = tests_module.ExecutionReplayer()
        trace = replayer.start_recording("test1")
        assert trace.test_id == "test1"

    def test_record_step(self, tests_module: Any) -> None:
        """Test recording a step."""
        replayer = tests_module.ExecutionReplayer()
        replayer.start_recording("test1")
        replayer.record_step("click", {"element": "button"})
        trace = replayer.stop_recording()
        assert len(trace.steps) == 1

    def test_replay(self, tests_module: Any) -> None:
        """Test replaying."""
        replayer = tests_module.ExecutionReplayer()
        replayer.start_recording("test1")
        replayer.record_step("click", {})
        replayer.stop_recording()
        replayed = replayer.replay("test1")
        assert len(replayed) == 1


# ========== Session 7 Tests: DependencyInjector ==========


class TestDependencyInjector:
    """Tests for DependencyInjector class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        injector = tests_module.DependencyInjector()
        assert injector.dependencies == {}

    def test_register(self, tests_module: Any) -> None:
        """Test registering dependency."""
        injector = tests_module.DependencyInjector()
        dep = injector.register("db", "Database", "MockDatabase()")
        assert dep.name == "db"

    def test_override(self, tests_module: Any) -> None:
        """Test overriding dependency."""
        injector = tests_module.DependencyInjector()
        injector.register("db", "Database")
        injector.override("db", "mock_db")
        resolved = injector.resolve("db")
        assert resolved == "mock_db"

    def test_get_fixture_code(self, tests_module: Any) -> None:
        """Test fixture code generation."""
        injector = tests_module.DependencyInjector()
        injector.register("db", "Database", "return MockDatabase()")
        code = injector.get_fixture_code("db")
        assert "@pytest.fixture" in code


# ========== Session 7 Tests: CrossBrowserRunner ==========


class TestCrossBrowserRunner:
    """Tests for CrossBrowserRunner class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        config = tests_module.CrossBrowserConfig(
            browsers=[tests_module.BrowserType.CHROME]
        )
        runner = tests_module.CrossBrowserRunner(config)
        assert len(runner.results) == 1

    def test_setup_driver(self, tests_module: Any) -> None:
        """Test driver setup."""
        config = tests_module.CrossBrowserConfig(
            browsers=[tests_module.BrowserType.CHROME]
        )
        runner = tests_module.CrossBrowserRunner(config)
        result = runner.setup_driver(tests_module.BrowserType.CHROME)
        assert result is True

    def test_get_summary(self, tests_module: Any) -> None:
        """Test getting summary."""
        config = tests_module.CrossBrowserConfig(
            browsers=[tests_module.BrowserType.CHROME]
        )
        runner = tests_module.CrossBrowserRunner(config)
        summary = runner.get_summary()
        assert "browsers" in summary


# ========== Session 7 Tests: ResultAggregator ==========


class TestResultAggregator:
    """Tests for ResultAggregator class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        aggregator = tests_module.ResultAggregator()
        assert aggregator.results == []

    def test_add_result(self, tests_module: Any) -> None:
        """Test adding result."""
        aggregator = tests_module.ResultAggregator()
        result = aggregator.add_result(
            tests_module.TestSourceType.PYTEST,
            "test_example",
            tests_module.TestStatus.PASSED,
            100.0
        )
        assert result.test_name == "test_example"

    def test_get_summary(self, tests_module: Any) -> None:
        """Test getting summary."""
        aggregator = tests_module.ResultAggregator()
        aggregator.add_result(
            tests_module.TestSourceType.PYTEST,
            "test1",
            tests_module.TestStatus.PASSED,
            100.0
        )
        summary = aggregator.get_summary()
        assert summary["total_tests"] == 1

    def test_export_unified_report(self, tests_module: Any) -> None:
        """Test exporting unified report."""
        aggregator = tests_module.ResultAggregator()
        aggregator.add_result(
            tests_module.TestSourceType.PYTEST,
            "test1",
            tests_module.TestStatus.PASSED,
            100.0
        )
        report = aggregator.export_unified_report()
        assert "summary" in report


# ========== Session 7 Tests: MutationTester ==========


class TestMutationTester:
    """Tests for MutationTester class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        tester = tests_module.MutationTester()
        assert tester.mutations == []

    def test_generate_mutations(self, tests_module: Any) -> None:
        """Test generating mutations."""
        tester = tests_module.MutationTester()
        code = "result=a + b"
        mutations = tester.generate_mutations(code, "test.py")
        assert len(mutations) >= 1

    def test_get_mutation_score(self, tests_module: Any) -> None:
        """Test getting mutation score."""
        tester = tests_module.MutationTester()
        code = "result=a + b"
        mutations = tester.generate_mutations(code, "test.py")
        for mut in mutations:
            tester.record_kill(mut.id, True)
        score = tester.get_mutation_score()
        assert score == 100.0

    def test_generate_report(self, tests_module: Any) -> None:
        """Test generating report."""
        tester = tests_module.MutationTester()
        tester.generate_mutations("a + b", "test.py")
        report = tester.generate_report()
        assert "Mutation Testing Report" in report


# ========== Session 7 Tests: TestGenerator ==========


class TestTestGenerator:
    """Tests for TestGenerator class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        generator = tests_module.TestGenerator()
        assert generator.generated == []

    def test_generate_from_spec(self, tests_module: Any) -> None:
        """Test generating from spec."""
        generator = tests_module.TestGenerator()
        generated = generator.generate_from_spec(
            "Should return sum of two numbers",
            "add"
        )
        assert "test_add" in generated.name

    def test_generate_parametrized(self, tests_module: Any) -> None:
        """Test generating parametrized test."""
        generator = tests_module.TestGenerator()
        generated = generator.generate_parametrized(
            "add",
            [(1, 1), (2, 4)]
        )
        assert "parametrize" in generated.generated_code

    def test_validate_generated(self, tests_module: Any) -> None:
        """Test validating generated test."""
        generator = tests_module.TestGenerator()
        generator.generate_from_spec("Test", "func")
        result = generator.validate_generated(0)
        assert result is True


# ========== Session 7 Tests: TestCaseMinimizer ==========


class TestTestCaseMinimizer:
    """Tests for TestCaseMinimizer class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        minimizer = tests_module.TestCaseMinimizer()
        assert minimizer.history == []

    def test_minimize_string(self, tests_module: Any) -> None:
        """Test minimizing string."""
        minimizer = tests_module.TestCaseMinimizer()
        # Test function that fails on strings containing 'x'
        result = minimizer.minimize_string(
            "abcxdef",
            lambda s: 'x' in s
        )
        assert 'x' in result
        assert len(result) <= len("abcxdef")

    def test_minimize_list(self, tests_module: Any) -> None:
        """Test minimizing list."""
        minimizer = tests_module.TestCaseMinimizer()
        result = minimizer.minimize_list(
            [1, 2, 3, 4, 5],
            lambda lst: 3 in lst
        )
        assert 3 in result

    def test_get_minimization_stats(self, tests_module: Any) -> None:
        """Test getting stats."""
        minimizer = tests_module.TestCaseMinimizer()
        stats = minimizer.get_minimization_stats()
        assert stats["total"] == 0


# ========== Session 7 Tests: TestProfiler ==========


class TestTestProfiler:
    """Tests for TestProfiler class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        profiler = tests_module.TestProfiler()
        assert profiler.profiles == {}

    def test_start_stop_profiling(self, tests_module: Any) -> None:
        """Test start / stop profiling."""
        profiler = tests_module.TestProfiler()
        profiler.start_profiling("test1")
        profile = profiler.stop_profiling("test1", memory_peak_mb=50.0)
        assert profile.test_id == "test1"
        assert profile.cpu_time_ms >= 0

    def test_get_slowest_tests(self, tests_module: Any) -> None:
        """Test getting slowest tests."""
        profiler = tests_module.TestProfiler()
        profiler.start_profiling("test1")
        profiler.stop_profiling("test1")
        slowest = profiler.get_slowest_tests(5)
        assert len(slowest) == 1

    def test_generate_report(self, tests_module: Any) -> None:
        """Test generating report."""
        profiler = tests_module.TestProfiler()
        profiler.start_profiling("test1")
        profiler.stop_profiling("test1")
        report = profiler.generate_report()
        assert "Profiling Report" in report


# ========== Session 7 Tests: TestScheduler ==========


class TestTestScheduler:
    """Tests for TestScheduler class."""

    def test_init(self, tests_module: Any) -> None:
        """Test initialization."""
        scheduler = tests_module.TestScheduler(num_workers=4)
        assert scheduler.num_workers == 4

    def test_add_duration_estimate(self, tests_module: Any) -> None:
        """Test adding duration estimate."""
        scheduler = tests_module.TestScheduler()
        scheduler.add_duration_estimate("test1", 1000.0)
        assert "test1" in scheduler._test_durations

    def test_create_schedule(self, tests_module: Any) -> None:
        """Test creating schedule."""
        scheduler = tests_module.TestScheduler(num_workers=2)
        scheduler.add_duration_estimate("test1", 1000.0)
        scheduler.add_duration_estimate("test2", 500.0)
        schedule = scheduler.create_schedule(["test1", "test2"], "10:00")
        assert len(schedule) >= 1

    def test_estimate_total_duration(self, tests_module: Any) -> None:
        """Test estimating total duration."""
        scheduler = tests_module.TestScheduler(num_workers=2)
        scheduler.add_duration_estimate("test1", 1000.0)
        scheduler.create_schedule(["test1"], "10:00")
        duration = scheduler.estimate_total_duration()
        assert duration >= 1000.0

    def test_get_worker_assignments(self, tests_module: Any) -> None:
        """Test getting worker assignments."""
        scheduler = tests_module.TestScheduler(num_workers=2)
        scheduler.create_schedule(["test1", "test2"], "10:00")
        assignments = scheduler.get_worker_assignments()
        assert isinstance(assignments, dict)


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================


class TestTestPrioritizationAlgorithms:
    """Tests for test prioritization algorithms."""

    def test_prioritizer_by_recent_changes(self, tests_module: Any) -> None:
        """Test prioritization by recent changes."""
        TestPrioritizer = tests_module.TestPrioritizer

        prioritizer = TestPrioritizer()
        prioritizer.add_test("test1", changed_recently=True)
        prioritizer.add_test("test2", changed_recently=False)
        prioritizer.add_test("test3", changed_recently=True)

        ordered = prioritizer.prioritize_by_changes()
        # Recently changed tests should come first
        assert ordered[0] in ["test1", "test3"]

    def test_prioritizer_by_failure_history(self, tests_module: Any) -> None:
        """Test prioritization by failure history."""
        TestPrioritizer = tests_module.TestPrioritizer

        prioritizer = TestPrioritizer()
        prioritizer.add_test("test1", failure_rate=0.8)
        prioritizer.add_test("test2", failure_rate=0.1)
        prioritizer.add_test("test3", failure_rate=0.5)

        ordered = prioritizer.prioritize_by_failure_rate()
        assert ordered[0] == "test1"  # Highest failure rate first

    def test_prioritizer_combined_strategy(self, tests_module: Any) -> None:
        """Test combined prioritization strategy."""
        TestPrioritizer = tests_module.TestPrioritizer

        prioritizer = TestPrioritizer()
        prioritizer.add_test("test1", changed_recently=False, failure_rate=0.9)
        prioritizer.add_test("test2", changed_recently=True, failure_rate=0.1)

        ordered = prioritizer.prioritize_combined(change_weight=0.5, failure_weight=0.5)
        assert len(ordered) == 2


class TestFlakinessDetectionAndQuarantine:
    """Tests for flakiness detection and quarantine."""

    def test_flakiness_detector_identifies_flaky(self, tests_module: Any) -> None:
        """Test flakiness detector identifies flaky tests."""
        FlakinessDetector = tests_module.FlakinessDetector

        detector = FlakinessDetector()
        # Add inconsistent results
        detector.record_result("test1", passed=True)
        detector.record_result("test1", passed=False)
        detector.record_result("test1", passed=True)
        detector.record_result("test1", passed=False)

        assert detector.is_flaky("test1")

    def test_flakiness_detector_stable_test(self, tests_module: Any) -> None:
        """Test flakiness detector identifies stable tests."""
        FlakinessDetector = tests_module.FlakinessDetector

        detector = FlakinessDetector()
        for _ in range(10):
            detector.record_result("test_stable", passed=True)

        assert not detector.is_flaky("test_stable")

    def test_quarantine_manager(self, tests_module: Any) -> None:
        """Test quarantine manager."""
        QuarantineManager = tests_module.QuarantineManager

        manager = QuarantineManager()
        manager.quarantine("flaky_test1", reason="Flaky for 7 days")

        assert manager.is_quarantined("flaky_test1")
        assert not manager.is_quarantined("stable_test")


class TestTestImpactAnalysis:
    """Tests for test impact analysis."""

    def test_impact_analyzer_file_changes(self, tests_module: Any) -> None:
        """Test impact analysis for file changes."""
        ImpactAnalyzer = tests_module.ImpactAnalyzer

        analyzer = ImpactAnalyzer()
        analyzer.map_test_to_files("test_auth", ["auth.py", "utils.py"])
        analyzer.map_test_to_files("test_db", ["database.py"])

        affected = analyzer.get_affected_tests(changed_files=["auth.py"])
        assert "test_auth" in affected
        assert "test_db" not in affected

    def test_impact_analyzer_dependency_graph(self, tests_module: Any) -> None:
        """Test impact analysis with dependency graph."""
        ImpactAnalyzer = tests_module.ImpactAnalyzer

        analyzer = ImpactAnalyzer()
        analyzer.add_dependency("utils.py", "auth.py")
        analyzer.map_test_to_files("test_auth", ["auth.py"])

        # Changing utils.py should affect test_auth via dependency
        affected = analyzer.get_affected_tests(
            changed_files=["utils.py"],
            include_dependencies=True
        )
        assert "test_auth" in affected


class TestDataFactoryIntegration:
    """Tests for data factory integration."""

    def test_data_factory_creates_objects(self, tests_module: Any) -> None:
        """Test data factory creates test objects."""
        DataFactory = tests_module.DataFactory

        factory = DataFactory()
        factory.register("user", {
            "id": "auto_increment",
            "name": "random_string",
            "email": "random_email"
        })

        user = factory.create("user")
        assert "id" in user
        assert "name" in user
        assert "@" in user["email"]

    def test_data_factory_with_overrides(self, tests_module: Any) -> None:
        """Test data factory with field overrides."""
        DataFactory = tests_module.DataFactory

        factory = DataFactory()
        factory.register("user", {"name": "random_string", "age": 25})

        user = factory.create("user", overrides={"name": "John", "age": 30})
        assert user["name"] == "John"
        assert user["age"] == 30

    def test_data_factory_batch_create(self, tests_module: Any) -> None:
        """Test data factory batch creation."""
        DataFactory = tests_module.DataFactory

        factory = DataFactory()
        factory.register("item", {"value": "random_int"})

        items = factory.create_batch("item", count=5)
        assert len(items) == 5


class TestTestParallelizationStrategies:
    """Tests for test parallelization strategies."""

    def test_round_robin_distribution(self, tests_module: Any) -> None:
        """Test round-robin test distribution."""
        ParallelizationStrategy = tests_module.ParallelizationStrategy

        strategy = ParallelizationStrategy("round_robin", workers=4)
        tests = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]

        distribution = strategy.distribute(tests)

        # Each worker should have 2 tests
        for worker_tests in distribution.values():
            assert len(worker_tests) == 2

    def test_load_balanced_distribution(self, tests_module: Any) -> None:
        """Test load-balanced test distribution."""
        ParallelizationStrategy = tests_module.ParallelizationStrategy

        strategy = ParallelizationStrategy("load_balanced", workers=2)
        tests = {"t1": 1000, "t2": 500, "t3": 200, "t4": 300}  # With durations

        distribution = strategy.distribute_balanced(tests)

        # Total time should be balanced between workers
        assert len(distribution) == 2


class TestCoverageGapAnalysis:
    """Tests for coverage gap analysis."""

    def test_gap_analyzer_finds_uncovered(self, tests_module: Any) -> None:
        """Test gap analyzer finds uncovered code."""
        CoverageGapAnalyzer = tests_module.CoverageGapAnalyzer

        analyzer = CoverageGapAnalyzer()
        analyzer.add_coverage_data("file.py", covered_lines={1, 2, 3, 5, 6})
        analyzer.set_total_lines("file.py", total_lines=10)

        gaps = analyzer.find_gaps("file.py")
        assert 4 in gaps
        assert 7 in gaps

    def test_gap_analyzer_coverage_percentage(self, tests_module: Any) -> None:
        """Test gap analyzer calculates percentage."""
        CoverageGapAnalyzer = tests_module.CoverageGapAnalyzer

        analyzer = CoverageGapAnalyzer()
        analyzer.add_coverage_data("file.py", covered_lines={1, 2, 3, 4, 5})
        analyzer.set_total_lines("file.py", total_lines=10)

        percentage = analyzer.get_coverage_percentage("file.py")
        assert percentage == 50.0


class TestContractTestingIntegration:
    """Tests for contract testing integration."""

    def test_contract_validator_valid(self, tests_module: Any) -> None:
        """Test contract validator with valid data."""
        ContractValidator = tests_module.ContractValidator

        validator = ContractValidator()
        contract = {
            "request": {"method": "GET", "path": "/users"},
            "response": {"status": 200, "body": {"type": "array"}}
        }

        result = validator.validate(
            contract,
            actual_response={"status": 200, "body": []}
        )
        assert result.valid

    def test_contract_validator_invalid(self, tests_module: Any) -> None:
        """Test contract validator with invalid data."""
        ContractValidator = tests_module.ContractValidator

        validator = ContractValidator()
        contract = {
            "response": {"status": 200}
        }

        result = validator.validate(
            contract,
            actual_response={"status": 404}
        )
        assert not result.valid


class TestTestSuiteOptimization:
    """Tests for test suite optimization."""

    def test_optimizer_removes_redundant(self, tests_module: Any) -> None:
        """Test optimizer removes redundant tests."""
        TestSuiteOptimizer = tests_module.TestSuiteOptimizer

        optimizer = TestSuiteOptimizer()
        optimizer.add_test("test1", covers={"func_a", "func_b"})
        optimizer.add_test("test2", covers={"func_a"})  # Redundant
        optimizer.add_test("test3", covers={"func_c"})

        optimized = optimizer.optimize()
        assert "test1" in optimized
        assert "test3" in optimized
        # test2 may be removed as redundant

    def test_optimizer_preserves_coverage(self, tests_module: Any) -> None:
        """Test optimizer preserves coverage."""
        TestSuiteOptimizer = tests_module.TestSuiteOptimizer

        optimizer = TestSuiteOptimizer()
        optimizer.add_test("test1", covers={"a", "b"})
        optimizer.add_test("test2", covers={"c", "d"})

        optimized = optimizer.optimize()
        total_coverage = set()
        for test in optimized:
            total_coverage.update(optimizer.get_coverage(test))

        assert total_coverage == {"a", "b", "c", "d"}


class TestEnvironmentProvisioningAutomation:
    """Tests for environment provisioning automation."""

    def test_provisioner_creates_environment(self, tests_module: Any) -> None:
        """Test provisioner creates test environment."""
        EnvironmentProvisioner = tests_module.EnvironmentProvisioner

        provisioner = EnvironmentProvisioner()
        env = provisioner.provision({
            "python_version": "3.11",
            "dependencies": ["pytest", "requests"]
        })

        assert env.status == "ready"
        assert "pytest" in env.dependencies

    def test_provisioner_cleanup(self, tests_module: Any) -> None:
        """Test provisioner cleans up environment."""
        EnvironmentProvisioner = tests_module.EnvironmentProvisioner

        provisioner = EnvironmentProvisioner()
        env = provisioner.provision({"python_version": "3.11"})

        provisioner.cleanup(env)
        assert env.status == "cleaned"


class TestTestReplayFunctionality:
    """Tests for test replay functionality."""

    def test_recorder_saves_execution(self, tests_module: Any) -> None:
        """Test recorder saves test execution."""
        TestRecorder = tests_module.TestRecorder

        recorder = TestRecorder()
        recorder.start_recording("test_example")
        recorder.record_action("call", {"func": "do_something", "args": [1, 2]})
        recorder.record_action("assert", {"expected": 3, "actual": 3})
        recording = recorder.stop_recording()

        assert len(recording.actions) == 2

    def test_replayer_executes_recording(self, tests_module: Any) -> None:
        """Test replayer executes recorded test."""
        TestReplayer = tests_module.TestReplayer
        TestRecorder = tests_module.TestRecorder

        # Create a recording
        recorder = TestRecorder()
        recorder.start_recording("test1")
        recorder.record_action("call", {"result": 42})
        recording = recorder.stop_recording()

        # Replay it
        replayer = TestReplayer()
        result = replayer.replay(recording)

        assert result.success


class TestDocumentationGenerationFromTests:
    """Tests for documentation generation from tests."""

    def test_doc_generator_extracts_examples(self, tests_module: Any) -> None:
        """Test doc generator extracts examples from tests."""
        TestDocGenerator = tests_module.TestDocGenerator

        generator = TestDocGenerator()
        generator.add_test(
            name="test_addition",
            docstring="Test that addition works.",
            code="assert 1 + 2 == 3"
        )

        docs = generator.generate()
        assert "addition" in docs.lower()
        assert "1 + 2" in docs

    def test_doc_generator_groups_by_module(self, tests_module: Any) -> None:
        """Test doc generator groups tests by module."""
        TestDocGenerator = tests_module.TestDocGenerator

        generator = TestDocGenerator()
        generator.add_test(name="test_a", module="module1")
        generator.add_test(name="test_b", module="module1")
        generator.add_test(name="test_c", module="module2")

        docs = generator.generate_grouped()
        assert "module1" in docs
        assert "module2" in docs


class TestDependencyInjectionPatterns:
    """Tests for dependency injection patterns in tests."""

    def test_di_container_registers_dependencies(self, tests_module: Any) -> None:
        """Test DI container registers dependencies."""
        DIContainer = tests_module.DIContainer

        container = DIContainer()
        container.register("database", lambda: {"connection": "mock"})
        container.register("cache", lambda: {"type": "memory"})

        assert container.has("database")
        assert container.has("cache")

    def test_di_container_resolves_dependencies(self, tests_module: Any) -> None:
        """Test DI container resolves dependencies."""
        DIContainer = tests_module.DIContainer

        container = DIContainer()
        container.register("config", lambda: {"timeout": 30})

        config = container.resolve("config")
        assert config["timeout"] == 30

    def test_di_container_with_test_overrides(self, tests_module: Any) -> None:
        """Test DI container supports test overrides."""
        DIContainer = tests_module.DIContainer

        container = DIContainer()
        container.register("service", lambda: {"real": True})

        with container.override("service", lambda: {"mock": True}):
            service = container.resolve("service")
            assert service["mock"] is True

        # Should be restored
        service = container.resolve("service")
        assert service["real"] is True


class TestTestResultAggregationExtended:
    """Tests for test result aggregation (extended)."""

    def test_aggregator_merges_multiple_runs(self, tests_module: Any) -> None:
        """Test aggregator merges results from multiple runs."""
        ResultAggregator = tests_module.ResultAggregator

        aggregator = ResultAggregator()
        aggregator.add_run({"passed": 10, "failed": 2, "skipped": 1})
        aggregator.add_run({"passed": 8, "failed": 4, "skipped": 0})

        merged = aggregator.merge()
        assert merged["total_passed"] == 18
        assert merged["total_failed"] == 6

    def test_aggregator_trend_analysis(self, tests_module: Any) -> None:
        """Test aggregator performs trend analysis."""
        ResultAggregator = tests_module.ResultAggregator

        aggregator = ResultAggregator()
        aggregator.add_run({"passed": 10, "failed": 5})
        aggregator.add_run({"passed": 12, "failed": 3})
        aggregator.add_run({"passed": 14, "failed": 1})

        trend = aggregator.get_trend()
        assert trend["pass_rate_trend"] == "improving"


class TestMutationTestingIntegration:
    """Tests for mutation testing integration."""

    def test_mutation_runner_applies_mutations(self, tests_module: Any) -> None:
        """Test mutation runner applies mutations."""
        MutationRunner = tests_module.MutationRunner

        runner = MutationRunner()
        mutations = runner.generate_mutations("x=1 + 2")

        assert any("1 - 2" in m or "-" in m for m in mutations)

    def test_mutation_runner_calculates_score(self, tests_module: Any) -> None:
        """Test mutation runner calculates mutation score."""
        MutationRunner = tests_module.MutationRunner

        runner = MutationRunner()
        runner.add_result("mutation1", killed=True)
        runner.add_result("mutation2", killed=True)
        runner.add_result("mutation3", killed=False)

        score = runner.get_mutation_score()
        assert score == pytest.approx(66.67, rel=0.1)


class TestTestMetricsCollection:
    """Tests for test metrics collection."""

    def test_metrics_collector_records_execution_time(self, tests_module: Any) -> None:
        """Test metrics collector records execution time."""
        TestMetricsCollector = tests_module.TestMetricsCollector

        collector = TestMetricsCollector()
        collector.record_execution("test1", duration_ms=150)
        collector.record_execution("test2", duration_ms=250)

        metrics = collector.get_metrics()
        assert metrics["total_duration_ms"] == 400
        assert metrics["average_duration_ms"] == 200

    def test_metrics_collector_tracks_flakiness(self, tests_module: Any) -> None:
        """Test metrics collector tracks flakiness."""
        TestMetricsCollector = tests_module.TestMetricsCollector

        collector = TestMetricsCollector()
        collector.record_flaky("test_flaky", occurrences=3)

        flaky_tests = collector.get_flaky_tests()
        assert "test_flaky" in flaky_tests


class TestTestBaselineManagement:
    """Tests for test baseline management."""

    def test_baseline_manager_saves_baseline(self, tests_module: Any, tmp_path: Path) -> None:
        """Test baseline manager saves baselines."""
        BaselineManager = tests_module.BaselineManager

        manager = BaselineManager(baseline_dir=tmp_path)
        manager.save_baseline("test_output", {"value": 42})

        loaded = manager.load_baseline("test_output")
        assert loaded["value"] == 42

    def test_baseline_manager_compares_to_baseline(self, tests_module: Any, tmp_path: Path) -> None:
        """Test baseline manager compares to baseline."""
        BaselineManager = tests_module.BaselineManager

        manager = BaselineManager(baseline_dir=tmp_path)
        manager.save_baseline("test_output", {"value": 42})

        result = manager.compare("test_output", {"value": 42})
        assert result.matches

    def test_baseline_manager_updates_baseline(self, tests_module: Any, tmp_path: Path) -> None:
        """Test baseline manager updates baselines."""
        BaselineManager = tests_module.BaselineManager

        manager = BaselineManager(baseline_dir=tmp_path)
        manager.save_baseline("test_output", {"value": 42})
        manager.update_baseline("test_output", {"value": 100})

        loaded = manager.load_baseline("test_output")
        assert loaded["value"] == 100
