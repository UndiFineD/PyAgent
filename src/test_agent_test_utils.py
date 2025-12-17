"""Tests for agent_test_utils.py."""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module, AGENT_DIR


@pytest.fixture
def utils_module() -> Any:
    """Load the agent_test_utils module for testing."""
    with agent_dir_on_path():
        return load_agent_module("agent_test_utils.py")


def test_agent_dir_on_path_modifies_sys_path() -> None:
    """Test that agent_dir_on_path adds AGENT_DIR to sys.path."""
    original_path = list(sys.path)
    with agent_dir_on_path():
        assert str(AGENT_DIR) in sys.path
        assert sys.path[0] == str(AGENT_DIR)

    # Should be restored
    assert sys.path == original_path


def test_load_agent_module_loads_valid_module() -> None:
    """Test loading a valid agent module."""
    # We can load this test file itself or another known file
    # But load_agent_module expects files in AGENT_DIR.
    # Let's try loading 'agent_test_utils.py' itself since it's in AGENT_DIR
    with agent_dir_on_path():
        mod = load_agent_module("agent_test_utils.py")
        assert mod.__name__ == "_dv_legacy_agent_test_utils"
        assert hasattr(mod, "agent_dir_on_path")


def test_load_agent_module_raises_on_missing_file() -> None:
    """Test that loading a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_agent_module("non_existent_file.py")


# =============================================================================
# Phase 6: Enum Tests
# =============================================================================


class TestTestStatusEnum:
    """Tests for TestStatus enum."""

    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values."""
        TestStatus = utils_module.TestStatus
        assert TestStatus.PASSED.value == "passed"
        assert TestStatus.FAILED.value == "failed"
        assert TestStatus.SKIPPED.value == "skipped"
        assert TestStatus.ERROR.value == "error"
        assert TestStatus.PENDING.value == "pending"


class TestMockResponseTypeEnum:
    """Tests for MockResponseType enum."""

    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values."""
        MockResponseType = utils_module.MockResponseType
        assert MockResponseType.SUCCESS.value == "success"
        assert MockResponseType.ERROR.value == "error"
        assert MockResponseType.TIMEOUT.value == "timeout"


class TestIsolationLevelEnum:
    """Tests for IsolationLevel enum."""

    def test_all_members(self, utils_module: Any) -> None:
        """Test all members exist."""
        IsolationLevel = utils_module.IsolationLevel
        members = [m.name for m in IsolationLevel]
        assert "NONE" in members
        assert "TEMP_DIR" in members
        assert "SANDBOX" in members


class TestTestDataTypeEnum:
    """Tests for TestDataType enum."""

    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values."""
        TestDataType = utils_module.TestDataType
        assert TestDataType.PYTHON_CODE.value == "python_code"
        assert TestDataType.MARKDOWN.value == "markdown"
        assert TestDataType.JSON.value == "json"


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================


class TestTestFixtureDataclass:
    """Tests for TestFixture dataclass."""

    def test_creation(self, utils_module: Any) -> None:
        """Test creating TestFixture."""
        TestFixture = utils_module.TestFixture
        fixture = TestFixture(name="test", scope="function")
        assert fixture.name == "test"
        assert fixture.scope == "function"
        assert fixture.setup_fn is None


class TestMockResponseDataclass:
    """Tests for MockResponse dataclass."""

    def test_creation_with_defaults(self, utils_module: Any) -> None:
        """Test creating MockResponse with defaults."""
        MockResponse = utils_module.MockResponse
        MockResponseType = utils_module.MockResponseType

        response = MockResponse()
        assert response.content == ""
        assert response.response_type == MockResponseType.SUCCESS
        assert response.latency_ms == 100


class TestTestResultDataclass:
    """Tests for TestResult dataclass."""

    def test_creation(self, utils_module: Any) -> None:
        """Test creating TestResult."""
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        result = TestResult(
            test_name="test_example",
            status=TestStatus.PASSED,
            duration_ms=150.5,
        )
        assert result.test_name == "test_example"
        assert result.status == TestStatus.PASSED
        assert result.duration_ms == 150.5


class TestPerformanceMetricDataclass:
    """Tests for PerformanceMetric dataclass."""

    def test_creation(self, utils_module: Any) -> None:
        """Test creating PerformanceMetric."""
        PerformanceMetric = utils_module.PerformanceMetric
        PerformanceMetricType = utils_module.PerformanceMetricType

        metric = PerformanceMetric(
            metric_type=PerformanceMetricType.EXECUTION_TIME,
            value=100.5,
            unit="ms",
            test_name="test_example",
        )
        assert metric.value == 100.5
        assert metric.unit == "ms"


class TestTestSnapshotDataclass:
    """Tests for TestSnapshot dataclass."""

    def test_auto_hash(self, utils_module: Any) -> None:
        """Test automatic hash generation."""
        TestSnapshot = utils_module.TestSnapshot

        snapshot = TestSnapshot(name="test", content="test content")
        assert snapshot.content_hash != ""
        assert len(snapshot.content_hash) == 64  # SHA256 hex


# =============================================================================
# Phase 6: MockAIBackend Tests
# =============================================================================


class TestMockAIBackend:
    """Tests for MockAIBackend class."""

    def test_initialization(self, utils_module: Any) -> None:
        """Test mock backend initialization."""
        MockAIBackend = utils_module.MockAIBackend
        mock = MockAIBackend()
        assert mock.get_call_history() == []

    def test_add_and_call_response(self, utils_module: Any) -> None:
        """Test adding and calling mock response."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.add_response("test", MockResponse(content="response", latency_ms=0))

        result = mock.call("test prompt")
        assert result == "response"

    def test_default_response(self, utils_module: Any) -> None:
        """Test default response for unmatched prompts."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.set_default_response(MockResponse(content="default", latency_ms=0))

        result = mock.call("unmatched prompt")
        assert result == "default"

    def test_timeout_response(self, utils_module: Any) -> None:
        """Test timeout response raises."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse
        MockResponseType = utils_module.MockResponseType

        mock = MockAIBackend()
        mock.add_response(
            "timeout",
            MockResponse(response_type=MockResponseType.TIMEOUT, latency_ms=0),
        )

        with pytest.raises(TimeoutError):
            mock.call("timeout")

    def test_call_history(self, utils_module: Any) -> None:
        """Test call history tracking."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.set_default_response(MockResponse(content="r", latency_ms=0))

        mock.call("prompt1")
        mock.call("prompt2")

        history = mock.get_call_history()
        assert len(history) == 2
        assert history[0][0] == "prompt1"
        assert history[1][0] == "prompt2"


# =============================================================================
# Phase 6: FixtureGenerator Tests
# =============================================================================


class TestFixtureGenerator:
    """Tests for FixtureGenerator class."""

    def test_initialization(self, utils_module: Any, tmp_path: Path) -> None:
        """Test fixture generator initialization."""
        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)
        assert gen.base_dir == tmp_path

    def test_create_python_file_fixture(self, utils_module: Any, tmp_path: Path) -> None:
        """Test creating Python file fixture."""
        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)

        fixture = gen.create_python_file_fixture("test.py", "print('hello')")
        assert fixture.name == "test.py"

        # Run setup
        path = fixture.setup_fn()
        assert path.exists()
        assert path.read_text() == "print('hello')"

        # Run teardown
        fixture.teardown_fn(path)
        assert not path.exists()

    def test_create_directory_fixture(self, utils_module: Any, tmp_path: Path) -> None:
        """Test creating directory fixture."""
        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)

        fixture = gen.create_directory_fixture("test_dir", {
            "file1.py": "content1",
            "file2.py": "content2",
        })

        path = fixture.setup_fn()
        assert path.exists()
        assert (path / "file1.py").read_text() == "content1"


# =============================================================================
# Phase 6: TestDataGenerator Tests
# =============================================================================


class TestTestDataGenerator:
    """Tests for TestDataGenerator class."""

    def test_generate_python_code(self, utils_module: Any) -> None:
        """Test generating Python code."""
        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        code = gen.generate_python_code(num_functions=2)
        assert "def function_0" in code
        assert "def function_1" in code

    def test_generate_python_with_docstrings(self, utils_module: Any) -> None:
        """Test generating Python with docstrings."""
        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        code = gen.generate_python_code(with_docstrings=True)
        assert '"""' in code

    def test_generate_markdown(self, utils_module: Any) -> None:
        """Test generating markdown."""
        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        md = gen.generate_markdown(num_sections=2)
        assert "# Test Document" in md
        assert "## Section" in md

    def test_generate_json(self, utils_module: Any) -> None:
        """Test generating JSON."""
        import json
        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        json_str = gen.generate_json(num_items=3)
        data = json.loads(json_str)
        assert len(data["items"]) == 3


# =============================================================================
# Phase 6: FileSystemIsolator Tests
# =============================================================================


class TestFileSystemIsolator:
    """Tests for FileSystemIsolator class."""

    def test_context_manager(self, utils_module: Any) -> None:
        """Test context manager functionality."""
        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as fs:
            temp_dir = fs.get_temp_dir()
            assert temp_dir is not None
            assert temp_dir.exists()

        # Should be cleaned up
        assert not temp_dir.exists()

    def test_write_and_read_file(self, utils_module: Any) -> None:
        """Test writing and reading files."""
        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as fs:
            fs.write_file("test.txt", "content")
            content = fs.read_file("test.txt")
            assert content == "content"


# =============================================================================
# Phase 6: PerformanceTracker Tests
# =============================================================================


class TestPerformanceTracker:
    """Tests for PerformanceTracker class."""

    def test_initialization(self, utils_module: Any) -> None:
        """Test tracker initialization."""
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()
        assert tracker.get_metrics() == []

    def test_track_execution(self, utils_module: Any) -> None:
        """Test tracking execution time."""
        import time
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test_func"):
            time.sleep(0.01)  # 10ms

        metrics = tracker.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].test_name == "test_func"
        assert metrics[0].value >= 10  # At least 10ms

    def test_get_summary(self, utils_module: Any) -> None:
        """Test getting performance summary."""
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test1"):
            pass
        with tracker.track("test2"):
            pass

        summary = tracker.get_summary()
        assert summary["total_metrics"] == 2


# =============================================================================
# Phase 6: SnapshotManager Tests
# =============================================================================


class TestSnapshotManager:
    """Tests for SnapshotManager class."""

    def test_initialization(self, utils_module: Any, tmp_path: Path) -> None:
        """Test snapshot manager initialization."""
        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)
        assert mgr.snapshot_dir == tmp_path

    def test_save_and_load_snapshot(self, utils_module: Any, tmp_path: Path) -> None:
        """Test saving and loading snapshots."""
        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        mgr.save_snapshot("test", "content")
        loaded = mgr.load_snapshot("test")

        assert loaded is not None
        assert loaded.content == "content"

    def test_assert_match_creates_snapshot(self, utils_module: Any, tmp_path: Path) -> None:
        """Test assert_match creates snapshot if missing."""
        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        result = mgr.assert_match("new_snapshot", "content")
        assert result is True

        loaded = mgr.load_snapshot("new_snapshot")
        assert loaded.content == "content"

    def test_assert_match_detects_mismatch(self, utils_module: Any, tmp_path: Path) -> None:
        """Test assert_match detects mismatch."""
        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        mgr.save_snapshot("test", "original")
        result = mgr.assert_match("test", "different")

        assert result is False


# =============================================================================
# Phase 6: TestResultAggregator Tests
# =============================================================================


class TestTestResultAggregator:
    """Tests for TestResultAggregator class."""

    def test_initialization(self, utils_module: Any) -> None:
        """Test aggregator initialization."""
        TestResultAggregator = utils_module.TestResultAggregator
        agg = TestResultAggregator()
        assert agg.get_results() == []

    def test_add_and_get_results(self, utils_module: Any) -> None:
        """Test adding and getting results."""
        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))
        agg.add_result(TestResult("test2", TestStatus.FAILED))

        assert len(agg.get_results()) == 2

    def test_get_report(self, utils_module: Any) -> None:
        """Test getting aggregated report."""
        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))
        agg.add_result(TestResult("test2", TestStatus.PASSED))
        agg.add_result(TestResult("test3", TestStatus.FAILED))

        report = agg.get_report()
        assert report["total"] == 3
        assert report["passed"] == 2
        assert report["failed"] == 1

    def test_get_failures(self, utils_module: Any) -> None:
        """Test getting failed tests."""
        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))
        agg.add_result(TestResult("test2", TestStatus.FAILED))

        failures = agg.get_failures()
        assert len(failures) == 1
        assert failures[0].test_name == "test2"


# =============================================================================
# Phase 6: AgentAssertions Tests
# =============================================================================


class TestAgentAssertions:
    """Tests for AgentAssertions class."""

    def test_assert_valid_python_passes(self, utils_module: Any) -> None:
        """Test assert_valid_python with valid code."""
        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        result = assertions.assert_valid_python("print('hello')")
        assert result is True

    def test_assert_valid_python_fails(self, utils_module: Any) -> None:
        """Test assert_valid_python with invalid code."""
        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        with pytest.raises(AssertionError):
            assertions.assert_valid_python("print(")

    def test_assert_contains_docstring(self, utils_module: Any) -> None:
        """Test assert_contains_docstring."""
        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        code_with_docstring = '"""Docstring."""\ndef foo(): pass'
        result = assertions.assert_contains_docstring(code_with_docstring)
        assert result is True

    def test_assert_json_valid(self, utils_module: Any) -> None:
        """Test assert_json_valid."""
        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        result = assertions.assert_json_valid('{"key": "value"}')
        assert result is True

    def test_assert_json_invalid(self, utils_module: Any) -> None:
        """Test assert_json_valid with invalid JSON."""
        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        with pytest.raises(AssertionError):
            assertions.assert_json_valid("{invalid json}")


# =============================================================================
# Phase 6: Integration Tests
# =============================================================================


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_mock_with_tracker(self, utils_module: Any) -> None:
        """Test mock backend with performance tracking."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse
        PerformanceTracker = utils_module.PerformanceTracker

        mock = MockAIBackend()
        mock.set_default_response(MockResponse(content="response", latency_ms=0))
        tracker = PerformanceTracker()

        with tracker.track("mock_call"):
            result = mock.call("test prompt")

        assert result == "response"
        metrics = tracker.get_metrics()
        assert len(metrics) == 1

    def test_fixture_with_isolation(self, utils_module: Any, tmp_path: Path) -> None:
        """Test fixture generator with file system isolation."""
        FixtureGenerator = utils_module.FixtureGenerator
        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as fs:
            temp_dir = fs.get_temp_dir()
            gen = FixtureGenerator(base_dir=temp_dir)

            fixture = gen.create_python_file_fixture("test.py", "print('test')")
            path = fixture.setup_fn()

            assert path.exists()
            assert "print" in path.read_text()

    def test_assertions_with_generated_data(self, utils_module: Any) -> None:
        """Test assertions with generated test data."""
        TestDataGenerator = utils_module.TestDataGenerator
        AgentAssertions = utils_module.AgentAssertions

        gen = TestDataGenerator()
        assertions = AgentAssertions()

        # Generate and validate Python code
        code = gen.generate_python_code(with_errors=False)
        assertions.assert_valid_python(code)

        # Generate and validate JSON
        json_data = gen.generate_json()
        assertions.assert_json_valid(json_data)

        all_assertions = assertions.get_assertions()
        assert len(all_assertions) == 2
        assert all(a.passed for a in all_assertions)


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================


class TestMockBackendResponseGeneration:
    """Tests for mock backend response generation."""

    def test_mock_response_with_custom_content(self, utils_module: Any) -> None:
        """Test mock response with custom content."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        custom_response = MockResponse(
            content="Custom generated content",
            latency_ms=50,
            tokens_used=100
        )
        mock.set_default_response(custom_response)

        result = mock.call("any prompt")
        assert result == "Custom generated content"

    def test_mock_response_sequence(self, utils_module: Any) -> None:
        """Test mock responses in sequence."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.add_response_sequence([
            MockResponse(content="First"),
            MockResponse(content="Second"),
            MockResponse(content="Third")
        ])

        assert mock.call("prompt") == "First"
        assert mock.call("prompt") == "Second"
        assert mock.call("prompt") == "Third"

    def test_mock_error_response(self, utils_module: Any) -> None:
        """Test mock error response generation."""
        MockAIBackend = utils_module.MockAIBackend
        MockResponseType = utils_module.MockResponseType

        mock = MockAIBackend()
        mock.set_error_response(MockResponseType.ERROR, "Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            mock.call("prompt")


class TestFixtureFactoryPatterns:
    """Tests for fixture factory patterns."""

    def test_fixture_factory_creates_agent_fixtures(self, utils_module: Any) -> None:
        """Test fixture factory creates agent fixtures."""
        FixtureFactory = utils_module.FixtureFactory

        factory = FixtureFactory()
        fixture = factory.create_agent_fixture(
            name="test_agent",
            config={"timeout": 30}
        )

        assert fixture.name == "test_agent"
        assert fixture.config["timeout"] == 30

    def test_fixture_factory_creates_file_fixtures(self, utils_module: Any, tmp_path: Path) -> None:
        """Test fixture factory creates file fixtures."""
        FixtureFactory = utils_module.FixtureFactory

        factory = FixtureFactory(base_dir=tmp_path)
        fixture = factory.create_file_fixture(
            name="test.py",
            content="# Test file"
        )

        path = fixture.setup_fn()
        assert path.exists()

    def test_fixture_factory_with_dependencies(self, utils_module: Any) -> None:
        """Test fixture factory with dependencies."""
        FixtureFactory = utils_module.FixtureFactory

        factory = FixtureFactory()
        parent = factory.create_agent_fixture(name="parent")
        child = factory.create_agent_fixture(
            name="child",
            dependencies=[parent]
        )

        assert len(child.dependencies) == 1


class TestTestDataSeedingUtilities:
    """Tests for test data seeding utilities."""

    def test_seeder_creates_reproducible_data(self, utils_module: Any) -> None:
        """Test seeder creates reproducible data with seed."""
        TestDataSeeder = utils_module.TestDataSeeder

        seeder1 = TestDataSeeder(seed=12345)
        seeder2 = TestDataSeeder(seed=12345)

        data1 = seeder1.generate_file_content()
        data2 = seeder2.generate_file_content()

        assert data1 == data2

    def test_seeder_creates_unique_data_without_seed(self, utils_module: Any) -> None:
        """Test seeder creates unique data without fixed seed."""
        TestDataSeeder = utils_module.TestDataSeeder

        seeder1 = TestDataSeeder()
        seeder2 = TestDataSeeder()

        data1 = seeder1.generate_unique_id()
        data2 = seeder2.generate_unique_id()

        # Should be different (with high probability)
        assert data1 != data2

    def test_seeder_bulk_data_generation(self, utils_module: Any) -> None:
        """Test bulk data generation."""
        TestDataSeeder = utils_module.TestDataSeeder

        seeder = TestDataSeeder()
        data = seeder.generate_bulk_data(count=10, data_type="python_code")

        assert len(data) == 10


class TestParallelTestExecutionHelpers:
    """Tests for parallel test execution helpers."""

    def test_parallel_runner_executes_tests(self, utils_module: Any) -> None:
        """Test parallel runner executes tests."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner(workers=2)

        results: list[str] = []

        def test_fn(name: str) -> str:
            results.append(name)
            return f"done_{name}"

        outputs = runner.run([
            lambda: test_fn("test1"),
            lambda: test_fn("test2")
        ])

        assert len(outputs) == 2

    def test_parallel_runner_collects_failures(self, utils_module: Any) -> None:
        """Test parallel runner collects failures."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner(workers=2)

        def failing_test() -> str:
            raise ValueError("Test failed")

        def passing_test() -> str:
            return "passed"

        runner.run([failing_test, passing_test], fail_fast=False)

        assert runner.failure_count == 1
        assert runner.success_count == 1


class TestTestOutputFormattingUtilities:
    """Tests for test output formatting utilities."""

    def test_formatter_formats_success(self, utils_module: Any) -> None:
        """Test formatter formats success output."""
        TestOutputFormatter = utils_module.TestOutputFormatter
        TestStatus = utils_module.TestStatus

        formatter = TestOutputFormatter()
        output = formatter.format_result(
            test_name="test_example",
            status=TestStatus.PASSED,
            duration_ms=150
        )

        assert "test_example" in output
        assert "PASSED" in output or "passed" in output.lower()

    def test_formatter_formats_failure_with_details(self, utils_module: Any) -> None:
        """Test formatter formats failure with details."""
        TestOutputFormatter = utils_module.TestOutputFormatter
        TestStatus = utils_module.TestStatus

        formatter = TestOutputFormatter()
        output = formatter.format_result(
            test_name="test_failing",
            status=TestStatus.FAILED,
            duration_ms=50,
            error_message="Assertion failed"
        )

        assert "Assertion failed" in output

    def test_formatter_summary_output(self, utils_module: Any) -> None:
        """Test formatter creates summary output."""
        TestOutputFormatter = utils_module.TestOutputFormatter

        formatter = TestOutputFormatter()
        formatter.add_result("test1", "passed", 100)
        formatter.add_result("test2", "failed", 50)
        formatter.add_result("test3", "passed", 75)

        summary = formatter.get_summary()
        assert summary["passed"] == 2
        assert summary["failed"] == 1


class TestAssertionHelperFunctions:
    """Tests for assertion helper functions."""

    def test_assert_file_contains(self, utils_module: Any, tmp_path: Path) -> None:
        """Test assert_file_contains helper."""
        AssertionHelpers = utils_module.AssertionHelpers

        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        helpers = AssertionHelpers()
        result = helpers.assert_file_contains(test_file, "Hello")
        assert result is True

    def test_assert_output_matches_pattern(self, utils_module: Any) -> None:
        """Test assert_output_matches_pattern helper."""
        AssertionHelpers = utils_module.AssertionHelpers

        helpers = AssertionHelpers()
        result = helpers.assert_output_matches_pattern(
            output="Error on line 42: syntax error",
            pattern=r"Error on line \d+:"
        )
        assert result is True

    def test_assert_raises_with_message(self, utils_module: Any) -> None:
        """Test assert_raises_with_message helper."""
        AssertionHelpers = utils_module.AssertionHelpers

        helpers = AssertionHelpers()

        def raising_fn() -> None:
            raise ValueError("Expected error message")

        result = helpers.assert_raises_with_message(
            raising_fn,
            ValueError,
            "Expected error"
        )
        assert result is True


class TestTestTimingAndBenchmarkingUtilities:
    """Tests for test timing and benchmarking utilities."""

    def test_timer_measures_duration(self, utils_module: Any) -> None:
        """Test timer measures execution duration."""
        TestTimer = utils_module.TestTimer
        import time

        timer = TestTimer()
        timer.start()
        time.sleep(0.01)  # 10ms
        timer.stop()

        duration = timer.elapsed_ms
        assert duration >= 10

    def test_benchmarker_multiple_runs(self, utils_module: Any) -> None:
        """Test benchmarker runs multiple iterations."""
        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()

        counter = {"count": 0}

        def test_fn() -> int:
            counter["count"] += 1
            return counter["count"]

        results = benchmarker.run(test_fn, iterations=5)

        assert counter["count"] == 5
        assert "average_ms" in results
        assert "min_ms" in results
        assert "max_ms" in results

    def test_benchmarker_statistics(self, utils_module: Any) -> None:
        """Test benchmarker calculates statistics."""
        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()
        results = benchmarker.run(lambda: 1 + 1, iterations=10)

        assert results["iterations"] == 10
        assert results["average_ms"] >= 0


class TestTestResultAggregationHelpers:
    """Tests for test result aggregation helpers."""

    def test_aggregator_combines_results(self, utils_module: Any) -> None:
        """Test aggregator combines results from multiple sources."""
        TestResultAggregator = utils_module.TestResultAggregator

        aggregator = TestResultAggregator()
        aggregator.add_result("suite1", "test1", "passed")
        aggregator.add_result("suite1", "test2", "failed")
        aggregator.add_result("suite2", "test1", "passed")

        summary = aggregator.get_summary()
        assert summary["total"] == 3
        assert summary["passed"] == 2
        assert summary["failed"] == 1

    def test_aggregator_by_suite(self, utils_module: Any) -> None:
        """Test aggregator groups by suite."""
        TestResultAggregator = utils_module.TestResultAggregator

        aggregator = TestResultAggregator()
        aggregator.add_result("suite1", "test1", "passed")
        aggregator.add_result("suite1", "test2", "passed")
        aggregator.add_result("suite2", "test1", "failed")

        by_suite = aggregator.get_by_suite()
        assert by_suite["suite1"]["total"] == 2
        assert by_suite["suite2"]["total"] == 1


class TestTestEnvironmentDetection:
    """Tests for test environment detection."""

    def test_env_detector_identifies_ci(self, utils_module: Any) -> None:
        """Test environment detector identifies CI."""
        EnvironmentDetector = utils_module.EnvironmentDetector

        detector = EnvironmentDetector()
        env = detector.detect()

        assert "is_ci" in env
        assert isinstance(env["is_ci"], bool)

    def test_env_detector_identifies_os(self, utils_module: Any) -> None:
        """Test environment detector identifies OS."""
        EnvironmentDetector = utils_module.EnvironmentDetector

        detector = EnvironmentDetector()
        env = detector.detect()

        assert "os" in env
        assert env["os"] in ["windows", "linux", "darwin", "unknown"]

    def test_env_detector_python_version(self, utils_module: Any) -> None:
        """Test environment detector gets Python version."""
        EnvironmentDetector = utils_module.EnvironmentDetector

        detector = EnvironmentDetector()
        env = detector.detect()

        assert "python_version" in env
        assert env["python_version"].startswith("3.")


class TestSnapshotComparisonUtilities:
    """Tests for test snapshot comparison utilities."""

    def test_snapshot_save_and_load(self, utils_module: Any, tmp_path: Path) -> None:
        """Test snapshot save and load."""
        SnapshotManager = utils_module.SnapshotManager

        manager = SnapshotManager(snapshot_dir=tmp_path)

        data = {"key": "value", "list": [1, 2, 3]}
        manager.save_snapshot("test_snapshot", data)

        loaded = manager.load_snapshot("test_snapshot")
        assert loaded == data

    def test_snapshot_comparison_matches(self, utils_module: Any, tmp_path: Path) -> None:
        """Test snapshot comparison when matching."""
        SnapshotManager = utils_module.SnapshotManager

        manager = SnapshotManager(snapshot_dir=tmp_path)

        data = {"key": "value"}
        manager.save_snapshot("test", data)

        result = manager.compare_snapshot("test", data)
        assert result.matches is True

    def test_snapshot_comparison_differs(self, utils_module: Any, tmp_path: Path) -> None:
        """Test snapshot comparison when different."""
        SnapshotManager = utils_module.SnapshotManager

        manager = SnapshotManager(snapshot_dir=tmp_path)

        manager.save_snapshot("test", {"key": "original"})
        result = manager.compare_snapshot("test", {"key": "changed"})

        assert result.matches is False
        assert result.diff is not None


class TestTestCoverageMeasurementHelpers:
    """Tests for test coverage measurement helpers."""

    def test_coverage_tracker_records_hits(self, utils_module: Any) -> None:
        """Test coverage tracker records function hits."""
        CoverageTracker = utils_module.CoverageTracker

        tracker = CoverageTracker()
        tracker.record_hit("module.function1")
        tracker.record_hit("module.function1")
        tracker.record_hit("module.function2")

        hits = tracker.get_hits()
        assert hits["module.function1"] == 2
        assert hits["module.function2"] == 1

    def test_coverage_tracker_percentage(self, utils_module: Any) -> None:
        """Test coverage percentage calculation."""
        CoverageTracker = utils_module.CoverageTracker

        tracker = CoverageTracker()
        tracker.register_target("func1")
        tracker.register_target("func2")
        tracker.record_hit("func1")

        percentage = tracker.get_percentage()
        assert percentage == 50.0


class TestTestLogCaptureUtilities:
    """Tests for test log capture utilities."""

    def test_log_capturer_captures_logs(self, utils_module: Any) -> None:
        """Test log capturer captures log messages."""
        LogCapturer = utils_module.LogCapturer
        import logging

        with LogCapturer() as capturer:
            logger = logging.getLogger("test_logger")
            logger.warning("Test warning message")

        logs = capturer.get_logs()
        assert any("Test warning" in log for log in logs)

    def test_log_capturer_filters_by_level(self, utils_module: Any) -> None:
        """Test log capturer filters by level."""
        LogCapturer = utils_module.LogCapturer
        import logging

        with LogCapturer(level=logging.ERROR) as capturer:
            logger = logging.getLogger("test_filter")
            logger.warning("Warning")
            logger.error("Error")

        logs = capturer.get_logs()
        assert any("Error" in log for log in logs)


class TestTestConfigurationLoadingUtilities:
    """Tests for test configuration loading utilities."""

    def test_config_loader_loads_json(self, utils_module: Any, tmp_path: Path) -> None:
        """Test config loader loads JSON files."""
        TestConfigLoader = utils_module.TestConfigLoader
        import json

        config_file = tmp_path / "test_config.json"
        config_file.write_text(json.dumps({"timeout": 30, "retries": 3}))

        loader = TestConfigLoader()
        config = loader.load(config_file)

        assert config["timeout"] == 30

    def test_config_loader_with_defaults(self, utils_module: Any, tmp_path: Path) -> None:
        """Test config loader applies defaults."""
        TestConfigLoader = utils_module.TestConfigLoader
        import json

        config_file = tmp_path / "partial_config.json"
        config_file.write_text(json.dumps({"timeout": 60}))

        loader = TestConfigLoader()
        config = loader.load(config_file, defaults={"timeout": 30, "retries": 5})

        assert config["timeout"] == 60  # Overridden
        assert config["retries"] == 5  # Default


class TestTestReportGenerationHelpers:
    """Tests for test report generation helpers."""

    def test_report_generator_creates_html(self, utils_module: Any, tmp_path: Path) -> None:
        """Test report generator creates HTML report."""
        TestReportGenerator = utils_module.TestReportGenerator

        generator = TestReportGenerator(output_dir=tmp_path)
        generator.add_test_result("test1", "passed", 100)
        generator.add_test_result("test2", "failed", 50, error="Assertion error")

        report_path = generator.generate_html()

        assert report_path.exists()
        content = report_path.read_text()
        assert "test1" in content
        assert "test2" in content

    def test_report_generator_creates_json(self, utils_module: Any, tmp_path: Path) -> None:
        """Test report generator creates JSON report."""
        TestReportGenerator = utils_module.TestReportGenerator
        import json

        generator = TestReportGenerator(output_dir=tmp_path)
        generator.add_test_result("test1", "passed", 100)

        report_path = generator.generate_json()

        assert report_path.exists()
        data = json.loads(report_path.read_text())
        assert "results" in data


class TestTestIsolationMechanisms:
    """Tests for test isolation mechanisms."""

    def test_isolator_creates_temp_directory(self, utils_module: Any) -> None:
        """Test isolator creates temporary directory."""
        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as isolator:
            temp_dir = isolator.get_temp_dir()
            assert temp_dir.exists()

            # Create file inside
            test_file = temp_dir / "test.txt"
            test_file.write_text("content")
            assert test_file.exists()

        # Should be cleaned up
        assert not temp_dir.exists()

    def test_isolator_preserves_environment(self, utils_module: Any) -> None:
        """Test isolator preserves environment."""
        EnvironmentIsolator = utils_module.EnvironmentIsolator
        import os

        original = os.environ.get("TEST_VAR", "")

        with EnvironmentIsolator() as isolator:
            isolator.set_env("TEST_VAR", "modified")
            assert os.environ.get("TEST_VAR") == "modified"

        # Should be restored
        assert os.environ.get("TEST_VAR", "") == original


class TestTestRetryUtilities:
    """Tests for test retry utilities."""

    def test_retry_on_failure(self, utils_module: Any) -> None:
        """Test retry mechanism on failure."""
        RetryHelper = utils_module.RetryHelper

        counter = {"attempts": 0}

        def flaky_fn() -> str:
            counter["attempts"] += 1
            if counter["attempts"] < 3:
                raise ValueError("Temporary failure")
            return "success"

        helper = RetryHelper(max_retries=5)
        result = helper.retry(flaky_fn)

        assert result == "success"
        assert counter["attempts"] == 3

    def test_retry_exhausted(self, utils_module: Any) -> None:
        """Test retry exhaustion."""
        RetryHelper = utils_module.RetryHelper

        def always_fails() -> None:
            raise ValueError("Always fails")

        helper = RetryHelper(max_retries=3)

        with pytest.raises(ValueError):
            helper.retry(always_fails)


class TestTestCleanupHooks:
    """Tests for test cleanup hooks."""

    def test_cleanup_hooks_execute(self, utils_module: Any) -> None:
        """Test cleanup hooks execute on exit."""
        CleanupManager = utils_module.CleanupManager

        manager = CleanupManager()
        cleaned: list[str] = []

        manager.register(lambda: cleaned.append("first"))
        manager.register(lambda: cleaned.append("second"))

        manager.cleanup()

        assert "first" in cleaned
        assert "second" in cleaned

    def test_cleanup_hooks_execute_in_order(self, utils_module: Any) -> None:
        """Test cleanup hooks execute in LIFO order."""
        CleanupManager = utils_module.CleanupManager

        manager = CleanupManager()
        order: list[int] = []

        manager.register(lambda: order.append(1))
        manager.register(lambda: order.append(2))
        manager.register(lambda: order.append(3))

        manager.cleanup()

        # Should be LIFO (last in, first out)
        assert order == [3, 2, 1]


class TestTestDependencyManagement:
    """Tests for test dependency management."""

    def test_dependency_resolver_orders_correctly(self, utils_module: Any) -> None:
        """Test dependency resolver orders tests correctly."""
        DependencyResolver = utils_module.DependencyResolver

        resolver = DependencyResolver()
        resolver.add_test("test_c", depends_on=["test_b"])
        resolver.add_test("test_b", depends_on=["test_a"])
        resolver.add_test("test_a", depends_on=[])

        order = resolver.resolve()

        assert order.index("test_a") < order.index("test_b")
        assert order.index("test_b") < order.index("test_c")

    def test_dependency_resolver_detects_cycle(self, utils_module: Any) -> None:
        """Test dependency resolver detects circular dependency."""
        DependencyResolver = utils_module.DependencyResolver

        resolver = DependencyResolver()
        resolver.add_test("test_a", depends_on=["test_b"])
        resolver.add_test("test_b", depends_on=["test_a"])

        with pytest.raises(ValueError, match="[Cc]ircular"):
            resolver.resolve()


class TestTestResourceAllocation:
    """Tests for test resource allocation."""

    def test_resource_pool_allocation(self, utils_module: Any) -> None:
        """Test resource pool allocates resources."""
        ResourcePool = utils_module.ResourcePool

        pool = ResourcePool(max_resources=3)

        r1 = pool.acquire("test1")
        r2 = pool.acquire("test2")

        assert r1 is not None
        assert r2 is not None
        assert pool.available == 1

    def test_resource_pool_release(self, utils_module: Any) -> None:
        """Test resource pool releases resources."""
        ResourcePool = utils_module.ResourcePool

        pool = ResourcePool(max_resources=2)

        r1 = pool.acquire("test1")
        assert pool.available == 1

        pool.release(r1)
        assert pool.available == 2

    def test_resource_pool_exhaustion(self, utils_module: Any) -> None:
        """Test resource pool handles exhaustion."""
        ResourcePool = utils_module.ResourcePool

        pool = ResourcePool(max_resources=1)

        r1 = pool.acquire("test1")
        r2 = pool.acquire("test2", timeout=0.1)  # Should timeout

        assert r1 is not None
        assert r2 is None  # No resource available


# =============================================================================
# Session 9: Parameterized Test Generator Tests
# =============================================================================


class TestParameterizedTestGenerator:
    """Tests for ParameterizedTestGenerator class."""

    def test_generator_init(self, utils_module: Any) -> None:
        """Test ParameterizedTestGenerator initialization."""
        ParameterizedTestGenerator = utils_module.ParameterizedTestGenerator

        gen = ParameterizedTestGenerator(test_name="my_test")
        assert gen.test_name == "my_test"

    def test_add_parameter(self, utils_module: Any) -> None:
        """Test adding parameters."""
        ParameterizedTestGenerator = utils_module.ParameterizedTestGenerator

        gen = ParameterizedTestGenerator()
        result = gen.add_parameter("size", [1, 2, 3])

        assert result is gen  # Returns self for chaining
        assert "size" in gen._parameters

    def test_generate_cases(self, utils_module: Any) -> None:
        """Test generating test cases."""
        ParameterizedTestGenerator = utils_module.ParameterizedTestGenerator

        gen = ParameterizedTestGenerator()
        gen.add_parameter("size", [1, 2])
        gen.add_parameter("mode", ["a", "b"])

        cases = gen.generate_cases()

        assert len(cases) == 4  # 2 * 2 combinations

    def test_generate_with_expected_fn(self, utils_module: Any) -> None:
        """Test generating with expected function."""
        ParameterizedTestGenerator = utils_module.ParameterizedTestGenerator

        gen = ParameterizedTestGenerator()
        gen.add_parameter("x", [1, 2])
        gen.set_expected_fn(lambda p: p["x"] * 2)

        cases = gen.generate_cases()

        assert cases[0].expected == 2
        assert cases[1].expected == 4


# =============================================================================
# Session 9: Dependency Container Tests
# =============================================================================


class TestDependencyContainer:
    """Tests for DependencyContainer class."""

    def test_container_init(self, utils_module: Any) -> None:
        """Test DependencyContainer initialization."""
        DependencyContainer = utils_module.DependencyContainer

        container = DependencyContainer()
        assert container._dependencies == {}

    def test_register_and_resolve(self, utils_module: Any) -> None:
        """Test registering and resolving dependency."""
        DependencyContainer = utils_module.DependencyContainer

        container = DependencyContainer()
        container.register("db", "mock_db")

        assert container.resolve("db") == "mock_db"

    def test_register_factory(self, utils_module: Any) -> None:
        """Test registering factory."""
        DependencyContainer = utils_module.DependencyContainer

        container = DependencyContainer()
        container.register_factory("counter", lambda: {"count": 0})

        result = container.resolve("counter")
        assert result == {"count": 0}

    def test_singleton_factory(self, utils_module: Any) -> None:
        """Test singleton factory returns same instance."""
        DependencyContainer = utils_module.DependencyContainer

        container = DependencyContainer()
        container.register_factory("singleton", lambda: object(), singleton=True)

        r1 = container.resolve("singleton")
        r2 = container.resolve("singleton")

        assert r1 is r2

    def test_resolve_not_found(self, utils_module: Any) -> None:
        """Test resolving unknown dependency raises KeyError."""
        DependencyContainer = utils_module.DependencyContainer

        container = DependencyContainer()

        with pytest.raises(KeyError):
            container.resolve("unknown")


# =============================================================================
# Session 9: Flakiness Detector Tests
# =============================================================================


class TestFlakinessDetector:
    """Tests for FlakinessDetector class."""

    def test_detector_init(self, utils_module: Any) -> None:
        """Test FlakinessDetector initialization."""
        FlakinessDetector = utils_module.FlakinessDetector

        detector = FlakinessDetector(default_runs=10)
        assert detector.default_runs == 10

    def test_analyze_stable_test(self, utils_module: Any) -> None:
        """Test analyzing stable test."""
        FlakinessDetector = utils_module.FlakinessDetector

        detector = FlakinessDetector()

        def stable_test():
            pass

        report = detector.analyze(stable_test, runs=5)

        assert report.passes == 5
        assert report.failures == 0
        assert report.flakiness_score == 0.0

    def test_analyze_failing_test(self, utils_module: Any) -> None:
        """Test analyzing always-failing test."""
        FlakinessDetector = utils_module.FlakinessDetector

        detector = FlakinessDetector()

        def failing_test():
            raise AssertionError("Always fails")

        report = detector.analyze(failing_test, runs=5)

        assert report.passes == 0
        assert report.failures == 5
        assert report.flakiness_score == 0.0  # Consistently failing

    def test_get_flaky_tests(self, utils_module: Any) -> None:
        """Test getting flaky tests."""
        FlakinessDetector = utils_module.FlakinessDetector

        detector = FlakinessDetector()

        # Run a stable test
        detector.analyze(lambda: None, runs=5, test_name="stable")

        flaky = detector.get_flaky_tests(threshold=0.1)
        assert "stable" not in flaky


# =============================================================================
# Session 9: Test Data Cleaner Tests
# =============================================================================


class TestTestDataCleaner:
    """Tests for TestDataCleaner class."""

    def test_cleaner_init(self, utils_module: Any) -> None:
        """Test TestDataCleaner initialization."""
        TestDataCleaner = utils_module.TestDataCleaner
        CleanupStrategy = utils_module.CleanupStrategy

        cleaner = TestDataCleaner(strategy=CleanupStrategy.DEFERRED)
        assert cleaner.strategy == CleanupStrategy.DEFERRED

    def test_register_and_cleanup_file(self, utils_module: Any, tmp_path) -> None:
        """Test registering and cleaning file."""
        TestDataCleaner = utils_module.TestDataCleaner

        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        cleaner = TestDataCleaner()
        cleaner.register_file(test_file)
        cleaned = cleaner.cleanup_all()

        assert cleaned == 1
        assert not test_file.exists()

    def test_register_callback(self, utils_module: Any) -> None:
        """Test registering cleanup callback."""
        TestDataCleaner = utils_module.TestDataCleaner

        cleaner = TestDataCleaner()
        callback_called = [False]
        cleaner.register_callback(lambda: callback_called.__setitem__(0, True))

        cleaner.cleanup_all()

        assert callback_called[0]

    def test_context_manager(self, utils_module: Any, tmp_path) -> None:
        """Test context manager behavior."""
        TestDataCleaner = utils_module.TestDataCleaner
        CleanupStrategy = utils_module.CleanupStrategy

        test_file = tmp_path / "ctx_test.txt"
        test_file.write_text("test")

        with TestDataCleaner(strategy=CleanupStrategy.IMMEDIATE) as cleaner:
            cleaner.register_file(test_file)

        assert not test_file.exists()


# =============================================================================
# Session 9: Cross-Platform Helper Tests
# =============================================================================


class TestCrossPlatformHelper:
    """Tests for CrossPlatformHelper class."""

    def test_helper_init(self, utils_module: Any) -> None:
        """Test CrossPlatformHelper initialization."""
        CrossPlatformHelper = utils_module.CrossPlatformHelper

        helper = CrossPlatformHelper()
        assert helper._platform is not None

    def test_platform_detection(self, utils_module: Any) -> None:
        """Test platform detection methods."""
        CrossPlatformHelper = utils_module.CrossPlatformHelper

        helper = CrossPlatformHelper()

        # At least one should be True
        is_known = helper.is_windows() or helper.is_linux() or helper.is_macos()
        assert is_known

    def test_normalize_path(self, utils_module: Any) -> None:
        """Test path normalization."""
        CrossPlatformHelper = utils_module.CrossPlatformHelper

        helper = CrossPlatformHelper()
        path = helper.normalize_path("./test")

        assert path.is_absolute()

    def test_normalize_line_endings(self, utils_module: Any) -> None:
        """Test line ending normalization."""
        CrossPlatformHelper = utils_module.CrossPlatformHelper

        helper = CrossPlatformHelper()
        content = "line1\r\nline2\rline3\n"
        normalized = helper.normalize_line_endings(content)

        # Should not have mixed line endings
        assert "\r\n" not in normalized or "\n" not in normalized.replace("\r\n", "")


# =============================================================================
# Session 9: Test Logger Tests
# =============================================================================


class TestTestLogger:
    """Tests for TestLogger class."""

    def test_logger_init(self, utils_module: Any) -> None:
        """Test TestLogger initialization."""
        TestLogger = utils_module.TestLogger

        logger = TestLogger()
        assert logger._logs == {}

    def test_capture_logs(self, utils_module: Any) -> None:
        """Test capturing logs."""
        TestLogger = utils_module.TestLogger

        logger = TestLogger()

        with logger.capture("test1"):
            logger.info("Test message")
            logger.debug("Debug message")

        logs = logger.get_logs("test1")
        assert len(logs) == 2

    def test_log_levels(self, utils_module: Any) -> None:
        """Test different log levels."""
        TestLogger = utils_module.TestLogger

        logger = TestLogger()

        with logger.capture("levels"):
            logger.debug("d")
            logger.info("i")
            logger.warning("w")
            logger.error("e")

        logs = logger.get_logs("levels")
        levels = [log.level for log in logs]

        assert "DEBUG" in levels
        assert "INFO" in levels
        assert "WARNING" in levels
        assert "ERROR" in levels

    def test_get_errors(self, utils_module: Any) -> None:
        """Test getting only error logs."""
        TestLogger = utils_module.TestLogger

        logger = TestLogger()

        with logger.capture("errors"):
            logger.info("info")
            logger.error("error1")
            logger.error("error2")

        errors = logger.get_errors("errors")
        assert len(errors) == 2


# =============================================================================
# Session 9: Parallel Test Runner Tests
# =============================================================================


class TestParallelTestRunner:
    """Tests for ParallelTestRunner class."""

    def test_runner_init(self, utils_module: Any) -> None:
        """Test ParallelTestRunner initialization."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner(workers=4)
        assert runner.workers == 4

    def test_add_and_run_tests(self, utils_module: Any) -> None:
        """Test adding and running tests."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner(workers=2)
        runner.add_test("test1", lambda: None)
        runner.add_test("test2", lambda: None)

        results = runner.run_all()

        assert len(results) == 2
        assert all(r.passed for r in results)

    def test_run_with_failure(self, utils_module: Any) -> None:
        """Test running with a failing test."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner()
        runner.add_test("pass", lambda: None)
        runner.add_test("fail", lambda: (_ for _ in ()).throw(AssertionError("fail")))

        results = runner.run_all()

        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]

        assert len(passed) == 1
        assert len(failed) == 1

    def test_get_summary(self, utils_module: Any) -> None:
        """Test getting execution summary."""
        ParallelTestRunner = utils_module.ParallelTestRunner

        runner = ParallelTestRunner()
        runner.add_test("t1", lambda: None)
        runner.add_test("t2", lambda: None)

        runner.run_all()
        summary = runner.get_summary()

        assert summary["total"] == 2
        assert summary["passed"] == 2


# =============================================================================
# Session 9: Test Recorder Tests
# =============================================================================


class TestTestRecorder:
    """Tests for TestRecorder class."""

    def test_recorder_init(self, utils_module: Any) -> None:
        """Test TestRecorder initialization."""
        TestRecorder = utils_module.TestRecorder

        recorder = TestRecorder()
        assert recorder._recordings == []

    def test_record_interaction(self, utils_module: Any) -> None:
        """Test recording interactions."""
        TestRecorder = utils_module.TestRecorder

        recorder = TestRecorder()

        with recorder.record():
            recorder.record_interaction("api", "get_data", (), {}, "result")

        assert len(recorder._recordings) == 1

    def test_replay_interaction(self, utils_module: Any) -> None:
        """Test replaying interactions."""
        TestRecorder = utils_module.TestRecorder

        recorder = TestRecorder()

        # Record
        with recorder.record():
            recorder.record_interaction("api", "call1", (), {}, "result1")

        # Replay
        with recorder.replay():
            result = recorder.get_replay_result("api", "call1")

        assert result == "result1"

    def test_save_and_load(self, utils_module: Any, tmp_path) -> None:
        """Test saving and loading recordings."""
        TestRecorder = utils_module.TestRecorder

        recorder = TestRecorder()
        save_path = tmp_path / "recording.json"

        with recorder.record():
            recorder.record_interaction("test", "fn", (1, 2), {"k": "v"}, "res")

        recorder.save(save_path)

        # New recorder loads
        recorder2 = TestRecorder()
        recorder2.load(save_path)

        assert len(recorder2._recordings) == 1


# =============================================================================
# Session 9: Baseline Manager Tests
# =============================================================================


class TestBaselineManager:
    """Tests for BaselineManager class."""

    def test_manager_init(self, utils_module: Any, tmp_path) -> None:
        """Test BaselineManager initialization."""
        BaselineManager = utils_module.BaselineManager

        manager = BaselineManager(tmp_path / "baselines")
        assert manager.baseline_dir.exists()

    def test_save_and_load_baseline(self, utils_module: Any, tmp_path) -> None:
        """Test saving and loading baseline."""
        BaselineManager = utils_module.BaselineManager

        manager = BaselineManager(tmp_path / "baselines")
        manager.save_baseline("perf", {"latency": 100, "memory": 50})

        loaded = manager.load_baseline("perf")

        assert loaded is not None
        assert loaded.values["latency"] == 100
        assert loaded.values["memory"] == 50

    def test_compare_no_change(self, utils_module: Any, tmp_path) -> None:
        """Test comparing with no change."""
        BaselineManager = utils_module.BaselineManager

        manager = BaselineManager(tmp_path / "baselines")
        manager.save_baseline("test", {"value": 100})

        result = manager.compare("test", {"value": 100})

        assert result["passed"]
        assert len(result["diffs"]) == 0

    def test_compare_with_change(self, utils_module: Any, tmp_path) -> None:
        """Test comparing with significant change."""
        BaselineManager = utils_module.BaselineManager

        manager = BaselineManager(tmp_path / "baselines")
        manager.save_baseline("test", {"value": 100})

        result = manager.compare("test", {"value": 150}, tolerance=0.1)

        assert not result["passed"]
        assert "value" in result["diffs"]


# =============================================================================
# Session 9: Test Profile Manager Tests
# =============================================================================


class TestTestProfileManager:
    """Tests for TestProfileManager class."""

    def test_manager_init(self, utils_module: Any) -> None:
        """Test TestProfileManager initialization."""
        TestProfileManager = utils_module.TestProfileManager

        manager = TestProfileManager()
        assert manager._profiles == {}

    def test_add_and_get_profile(self, utils_module: Any) -> None:
        """Test adding and getting profile."""
        TestProfileManager = utils_module.TestProfileManager
        TestProfile = utils_module.TestProfile

        manager = TestProfileManager()
        profile = TestProfile(name="ci", settings={"timeout": 60})
        manager.add_profile(profile)

        retrieved = manager.get_profile("ci")
        assert retrieved.settings["timeout"] == 60

    def test_activate_profile(self, utils_module: Any) -> None:
        """Test activating profile."""
        TestProfileManager = utils_module.TestProfileManager
        TestProfile = utils_module.TestProfile

        manager = TestProfileManager()
        manager.add_profile(TestProfile("test", settings={"key": "value"}))

        manager.activate("test")

        assert manager.get_setting("key") == "value"

    def test_deactivate_profile(self, utils_module: Any) -> None:
        """Test deactivating profile."""
        TestProfileManager = utils_module.TestProfileManager
        TestProfile = utils_module.TestProfile

        manager = TestProfileManager()
        manager.add_profile(TestProfile("test", settings={"key": "value"}))

        manager.activate("test")
        manager.deactivate()

        assert manager.get_active_profile() is None

    def test_get_setting_default(self, utils_module: Any) -> None:
        """Test getting setting with default."""
        TestProfileManager = utils_module.TestProfileManager

        manager = TestProfileManager()

        value = manager.get_setting("nonexistent", default="default")
        assert value == "default"
