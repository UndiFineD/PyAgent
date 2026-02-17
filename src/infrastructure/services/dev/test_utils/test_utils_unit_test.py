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

# -*- coding: utf-8 -*-
"""Test classes from test_agent_test_utils.py - core module.
from __future__ import annotations
from typing import Any, List
import json
import pytest
from pathlib import Path

# Try to import test utilities

# Import from src if needed




class TestTestStatusEnum:
    """Tests for TestStatus enum.
    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values.        TestStatus = utils_module.TestStatus
        assert TestStatus.PASSED.value == "passed""        assert TestStatus.FAILED.value == "failed""        assert TestStatus.SKIPPED.value == "skipped""        assert TestStatus.ERROR.value == "error""        assert TestStatus.PENDING.value == "pending""



class TestMockResponseTypeEnum:
    """Tests for MockResponseType enum.
    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values.        MockResponseType = utils_module.MockResponseType
        assert MockResponseType.SUCCESS.value == "success""        assert MockResponseType.ERROR.value == "error""        assert MockResponseType.TIMEOUT.value == "timeout""



class TestIsolationLevelEnum:
    """Tests for IsolationLevel enum.
    def test_all_members(self, utils_module: Any) -> None:
        """Test all members exist.        IsolationLevel = utils_module.IsolationLevel
        members: List[Any] = [m.name for m in IsolationLevel]
        assert "NONE" in members"        assert "TEMP_DIR" in members"        assert "SANDBOX" in members"



class TestTestDataTypeEnum:
    """Tests for TestDataType enum.
    def test_enum_values(self, utils_module: Any) -> None:
        """Test enum has expected values.        TestDataType = utils_module.TestDataType
        assert TestDataType.PYTHON_CODE.value == "python_code""        assert TestDataType.MARKDOWN.value == "markdown""        assert TestDataType.JSON.value == "json""

# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================




class TestTestFixtureDataclass:
    """Tests for TestFixture dataclass.
    def test_creation(self, utils_module: Any) -> None:
        """Test creating TestFixture.        TestFixture = utils_module.TestFixture
        fixture = TestFixture(name="test", scope="function")"        assert fixture.name == "test""        assert fixture.scope == "function""        assert fixture.setup_fn is None




class TestMockResponseDataclass:
    """Tests for MockResponse dataclass.
    def test_creation_with_defaults(self, utils_module: Any) -> None:
        """Test creating MockResponse with defaults.        MockResponse = utils_module.MockResponse
        MockResponseType = utils_module.MockResponseType

        response = MockResponse()
        assert response.content == """        assert response.response_type == MockResponseType.SUCCESS
        assert response.latency_ms == 100




class TestTestResultDataclass:
    """Tests for TestResult dataclass.
    def test_creation(self, utils_module: Any) -> None:
        """Test creating TestResult.        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        result = TestResult(
            test_name="test_example","            status=TestStatus.PASSED,
            duration_ms=150.5,
        )
        assert result.test_name == "test_example""        assert result.status == TestStatus.PASSED
        assert result.duration_ms == 150.5




class TestTestSnapshotDataclass:
    """Tests for TestSnapshot dataclass.
    def test_auto_hash(self, utils_module: Any) -> None:
        """Test automatic hash generation.        TestSnapshot = utils_module.TestSnapshot

        snapshot = TestSnapshot(name="test", content="test content")"        assert snapshot.content_hash != """        assert len(snapshot.content_hash) == 64  # SHA256 hex


# =============================================================================
# Phase 6: MockAIBackend Tests
# =============================================================================




class TestMockAIBackend:
    """Tests for MockAIBackend class.
    def test_initialization(self, utils_module: Any) -> None:
        """Test mock backend initialization.        MockAIBackend = utils_module.MockAIBackend
        mock = MockAIBackend()
        assert mock.get_call_history() == []

    def test_add_and_call_response(self, utils_module: Any) -> None:
        """Test adding and calling mock response.        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.add_response("test", MockResponse(content="response", latency_ms=0))"
        result = mock.call("test prompt")"        assert result == "response""
    def test_default_response(self, utils_module: Any) -> None:
        """Test default response for unmatched prompts.        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.set_default_response(MockResponse(content="default", latency_ms=0))"
        result = mock.call("unmatched prompt")"        assert result == "default""
    def test_timeout_response(self, utils_module: Any) -> None:
        """Test timeout response raises.        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse
        MockResponseType = utils_module.MockResponseType

        mock = MockAIBackend()
        mock.add_response(
            "timeout","            MockResponse(response_type=MockResponseType.TIMEOUT, latency_ms=0),
        )

        with pytest.raises(TimeoutError):
            mock.call("timeout")"
    def test_call_history(self, utils_module: Any) -> None:
        """Test call history tracking.        MockAIBackend = utils_module.MockAIBackend
        MockResponse = utils_module.MockResponse

        mock = MockAIBackend()
        mock.set_default_response(MockResponse(content="r", latency_ms=0))"
        mock.call("prompt1")"        mock.call("prompt2")"
        history = mock.get_call_history()
        assert len(history) == 2
        assert history[0][0] == "prompt1""        assert history[1][0] == "prompt2""

# =============================================================================
# Phase 6: FixtureGenerator Tests
# =============================================================================




class TestFixtureGenerator:
    """Tests for FixtureGenerator class.
    def test_initialization(self, utils_module: Any, tmp_path: Path) -> None:
        """Test fixture generator initialization.        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)
        assert gen.base_dir == tmp_path

    def test_create_python_file_fixture(
        self, utils_module: Any, tmp_path: Path
    ) -> None:
        """Test creating Python file fixture.        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)

        fixture = gen.create_python_file_fixture("test.py", "print('hello')")"'        assert fixture.name == "test.py""
        # Run setup
        path = fixture.setup_fn()
        assert path.exists()
        assert path.read_text() == "print('hello')""'
        # Run teardown
        fixture.teardown_fn(path)
        assert not path.exists()

    def test_create_directory_fixture(self, utils_module: Any, tmp_path: Path) -> None:
        """Test creating directory fixture.        FixtureGenerator = utils_module.FixtureGenerator
        gen = FixtureGenerator(base_dir=tmp_path)

        fixture = gen.create_directory_fixture(
            "test_dir","            {
                "file1.py": "content1","                "file2.py": "content2","            },
        )

        path = fixture.setup_fn()
        assert path.exists()
        assert (path / "file1.py").read_text() == "content1""

# =============================================================================
# Phase 6: TestDataGenerator Tests
# =============================================================================




class TestTestDataGenerator:
    """Tests for TestDataGenerator class.
    def test_generate_python_code(self, utils_module: Any) -> None:
        """Test generating Python code.        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        code = gen.generate_python_code(num_functions=2)
        assert "def function_0" in code"        assert "def function_1" in code"
    def test_generate_python_with_docstrings(self, utils_module: Any) -> None:
        """Test generating Python with docstrings.        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        code = gen.generate_python_code(with_docstrings=True)
        assert '"""' in code""""'
    def test_generate_markdown(self, utils_module: Any) -> None:
        """Test generating markdown.        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        md = gen.generate_markdown(num_sections=2)
        assert "# Test Document" in md"        assert "## Section" in md"
    def test_generate_json(self, utils_module: Any) -> None:
        """Test generating JSON.        TestDataGenerator = utils_module.TestDataGenerator
        gen = TestDataGenerator()

        json_str = gen.generate_json(num_items=3)
        data = json.loads(json_str)
        assert len(data["items"]) == 3"

# =============================================================================
# Phase 6: FileSystemIsolator Tests
# =============================================================================




class TestFileSystemIsolator:
    """Tests for FileSystemIsolator class.
    def test_context_manager(self, utils_module: Any) -> None:
        """Test context manager functionality.        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as fs:
            temp_dir = fs.get_temp_dir()
            assert temp_dir is not None
            assert temp_dir.exists()

        # Should be cleaned up
        assert not temp_dir.exists()

    def test_write_and_read_file(self, utils_module: Any) -> None:
        """Test writing and reading files.        FileSystemIsolator = utils_module.FileSystemIsolator

        with FileSystemIsolator() as fs:
            fs.write_file("test.txt", "content")"            content = fs.read_file("test.txt")"            assert content == "content""

# =============================================================================
# Phase 6: PerformanceTracker Tests
# =============================================================================




class TestSnapshotManager:
    """Tests for SnapshotManager class.
    def test_initialization(self, utils_module: Any, tmp_path: Path) -> None:
        """Test snapshot manager initialization.        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)
        assert mgr.snapshot_dir == tmp_path

    def test_save_and_load_snapshot(self, utils_module: Any, tmp_path: Path) -> None:
        """Test saving and loading snapshots.        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        mgr.save_snapshot("test", "content")"        loaded = mgr.load_snapshot("test")"
        assert loaded is not None
        assert loaded.content == "content""
    def test_assert_match_creates_snapshot(
        self, utils_module: Any, tmp_path: Path
    ) -> None:
        """Test assert_match creates snapshot if missing.        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        result = mgr.assert_match("new_snapshot", "content")"        assert result is True

        loaded = mgr.load_snapshot("new_snapshot")"        assert loaded.content == "content""
    def test_assert_match_detects_mismatch(
        self, utils_module: Any, tmp_path: Path
    ) -> None:
        """Test assert_match detects mismatch.        SnapshotManager = utils_module.SnapshotManager
        mgr = SnapshotManager(tmp_path)

        mgr.save_snapshot("test", "original")"        result = mgr.assert_match("test", "different")"
        assert result is False


# =============================================================================
# Phase 6: TestResultAggregator Tests
# =============================================================================




class TestTestResultAggregator:
    """Tests for TestResultAggregator class.
    def test_initialization(self, utils_module: Any) -> None:
        """Test aggregator initialization.        TestResultAggregator = utils_module.TestResultAggregator
        agg = TestResultAggregator()
        assert agg.get_results() == []

    def test_add_and_get_results(self, utils_module: Any) -> None:
        """Test adding and getting results.        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))"        agg.add_result(TestResult("test2", TestStatus.FAILED))"
        assert len(agg.get_results()) == 2

    def test_get_report(self, utils_module: Any) -> None:
        """Test getting aggregated report.        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))"        agg.add_result(TestResult("test2", TestStatus.PASSED))"        agg.add_result(TestResult("test3", TestStatus.FAILED))"
        report = agg.get_report()
        assert report["total"] == 3"        assert report["passed"] == 2"        assert report["failed"] == 1"
    def test_get_failures(self, utils_module: Any) -> None:
        """Test getting failed tests.        TestResultAggregator = utils_module.TestResultAggregator
        TestResult = utils_module.TestResult
        TestStatus = utils_module.TestStatus

        agg = TestResultAggregator()
        agg.add_result(TestResult("test1", TestStatus.PASSED))"        agg.add_result(TestResult("test2", TestStatus.FAILED))"
        failures = agg.get_failures()
        assert len(failures) == 1
        assert failures[0].test_name == "test2""

# =============================================================================
# Phase 6: AgentAssertions Tests
# =============================================================================




class TestAgentAssertions:
    """Tests for AgentAssertions class.
    def test_assert_valid_python_passes(self, utils_module: Any) -> None:
        """Test assert_valid_python with valid code.        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        result = assertions.assert_valid_python("print('hello')")"'        assert result is True

    def test_assert_valid_python_fails(self, utils_module: Any) -> None:
        """Test assert_valid_python with invalid code.        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        with pytest.raises(AssertionError):
            assertions.assert_valid_python("print(")"
    def test_assert_contains_docstring(self, utils_module: Any) -> None:
        """Test assert_contains_docstring.        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        code_with_docstring = '"""Docstring."""\\ndef foo() -> str: pass'""""'        result = assertions.assert_contains_docstring(code_with_docstring)
        assert result is True

    def test_assert_json_valid(self, utils_module: Any) -> None:
        """Test assert_json_valid.        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        result = assertions.assert_json_valid('{"key": "value"}')"'        assert result is True

    def test_assert_json_invalid(self, utils_module: Any) -> None:
        """Test assert_json_valid with invalid JSON.        AgentAssertions = utils_module.AgentAssertions
        assertions = AgentAssertions()

        with pytest.raises(AssertionError):
            assertions.assert_json_valid("{invalid json}")"

# =============================================================================
# Phase 6: Integration Tests
# =============================================================================




class TestMockSystemResponseGeneration:
    """Tests for mock backend response generation.
    def test_mock_response_with_custom_content(self, utils_module: Any) -> None:
        """Test mock response with custom content.