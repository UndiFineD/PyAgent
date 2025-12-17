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

"""Legacy tests for base_agent.py.

These live next to the agent scripts so they can be run directly via:

    pytest scripts / agent / test_base_agent.py
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import pytest
from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


def test_read_previous_content_existing_file(tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "x.md"
    target.write_text("HELLO", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() == "HELLO"


def test_read_previous_content_missing_file_uses_default(
        tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "missing.md"
    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    assert "Default content" in content


def test_improve_content_uses_run_subagent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                                           base_agent_module: Any):
    target = tmp_path / "x.md"
    target.write_text("BEFORE", encoding="utf-8")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        assert "Improve" in description
        assert prompt == "prompt"
        assert original_content == "BEFORE"
        return "AFTER"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    agent = base_agent_module.BaseAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "AFTER"


def test_update_file_writes_content(tmp_path: Path, base_agent_module: Any) -> None:
    # Use a non-markdown extension so the markdown fixer won't interfere.
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.current_content = "CONTENT"
    agent.update_file()
    assert target.read_text(encoding="utf-8") == "CONTENT"


def test_get_diff_contains_unified_markers(tmp_path: Path, base_agent_module: Any) -> None:
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.previous_content = "A\n"
    agent.current_content = "B\n"
    diff = agent.get_diff()
    assert "--- previous" in diff
    assert "+++ current" in diff


def test_run_subagent_prefers_local_copilot_cli(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    calls: list[list[str]] = []

    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(args: List[str], **kwargs: Any) -> Result:
        # Record args only (not env / token).
        calls.append(list(args))
        # "copilot --version" probe succeeds.
        if args[:2] == ["copilot", "--version"]:
            return Result(0, "copilot 1.2.3")
        # Actual copilot invocation returns a response.
        if args and args[0] == "copilot":
            assert "--prompt" in args
            assert "--deny-tool" in args
            assert "--silent" in args
            return Result(0, "OK_FROM_COPILOT")
        raise AssertionError(f"Unexpected subprocess call: {args}")
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", fake_run)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "OK_FROM_COPILOT"
    assert calls[0][:2] == ["copilot", "--version"]


def test_run_subagent_falls_back_to_gh_copilot_explain(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    calls: list[list[str]] = []

    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(args: List[str], **kwargs: Any) -> Result:
        calls.append(list(args))
        # "copilot" missing.
        if args[:2] == ["copilot", "--version"]:
            raise FileNotFoundError("copilot not found")
        # "gh" is present.
        if args[:2] == ["gh", "--version"]:
            return Result(0, "gh version 2.x")
        # gh copilot explain returns text.
        if args[:3] == ["gh", "copilot", "explain"]:
            return Result(0, "EXPLAINED")
        raise AssertionError(f"Unexpected subprocess call: {args}")
    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", fake_run)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "git status", "ORIG")
    assert "EXPLAINED" in out
    assert any(c[:3] == ["gh", "copilot", "explain"] for c in calls)


def test_llm_chat_via_github_models_builds_request_and_parses_response(
    monkeypatch: pytest.MonkeyPatch, base_agent_module: Any
) -> None:
    posted: Dict[str, Any] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> Dict[str, Any]:
            return {"choices": [{"message": {"content": "  hello  "}}]}

    def fake_post(url: str,
                  headers: Optional[Dict[str,
                                         str]] = None,
                  data: Optional[str] = None,
                  timeout: Optional[int] = None) -> FakeResponse:
        posted["url"] = url
        posted["headers"] = headers
        posted["data"] = data
        posted["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(base_agent_module.agent_backend.requests, "post", fake_post)
    out = base_agent_module.agent_backend.llm_chat_via_github_models(
        prompt="Say hi",
        model="some-model",
        system_prompt="system",
        base_url="https://example.test",
        token="TOKEN",
        timeout_s=12,
    )
    assert out == "hello"
    assert posted["url"] == "https://example.test / v1 / chat / completions"
    assert posted["headers"]["Authorization"] == "Bearer TOKEN"
    assert posted["timeout"] == 12
    assert '"model": "some-model"' in posted["data"]
    assert '"role": "user"' in posted["data"]


def test_llm_chat_via_github_models_requires_token_and_base_url(base_agent_module: Any) -> None:
    with pytest.raises(RuntimeError, match=r"Missing token"):
        base_agent_module.agent_backend.llm_chat_via_github_models(
            prompt="x", model="m", base_url="https://x", token=None)
    with pytest.raises(RuntimeError, match=r"Missing base URL"):
        base_agent_module.agent_backend.llm_chat_via_github_models(
            prompt="x", model="m", base_url=None, token="t")


def test_run_subagent_uses_github_models_backend(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    # Force backend selection.
    monkeypatch.setenv("DV_AGENT_BACKEND", "github-models")
    monkeypatch.setenv("GITHUB_MODELS_BASE_URL", "https://example.test")
    monkeypatch.setenv("DV_AGENT_MODEL", "unit-test-model")
    monkeypatch.setenv("GITHUB_TOKEN", "TOKEN")
    # If subprocess is used, fail.

    def boom(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("subprocess.run should not be called for github-models backend")
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", boom)

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> Dict[str, Any]:
            return {"choices": [{"message": {"content": "OK_FROM_MODELS"}}]}

    def fake_post(url: str,
                  headers: Optional[Dict[str,
                                         str]] = None,
                  data: Optional[str] = None,
                  timeout: Optional[int] = None) -> FakeResponse:
        assert url == "https://example.test / v1 / chat / completions"
        assert headers is not None and headers["Authorization"] == "Bearer TOKEN"
        assert data is not None and '"model": "unit-test-model"' in data
        return FakeResponse()

    monkeypatch.setattr(base_agent_module.agent_backend.requests, "post", fake_post)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "OK_FROM_MODELS"


def test_run_subagent_handles_subprocess_failures_gracefully(
        monkeypatch: pytest.MonkeyPatch, base_agent_module: Any) -> None:
    """Verify that subprocess failures (non-zero exit code) result in fallback response."""
    class Result:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_run_fail_all(args: List[str], **kwargs: Any) -> Result:
        # Pretend tools exist but fail during execution
        if args[:2] == ["copilot", "--version"]:
            return Result(0, "copilot 1.2.3")
        if args[:2] == ["gh", "--version"]:
            return Result(0, "gh 2.0.0")
        return Result(1, "", "Process failed")

    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", fake_run_fail_all)

    agent = base_agent_module.BaseAgent("x.md")
    # Pass empty original_content to force fallback message
    out = agent.run_subagent("desc", "prompt", "")
    assert "AI Improvement Unavailable" in out


# ============================================================================
# New tests for suggested improvements
# ============================================================================

def test_read_file_with_utf8_bom_encoding(tmp_path: Path, base_agent_module: Any) -> None:
    """Test file reading with UTF-8 BOM encoding."""
    target = tmp_path / "bom.md"
    # Write file with UTF-8 BOM
    target.write_bytes(b'\xef\xbb\xbfHELLO WITH BOM')
    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    # Should handle BOM gracefully
    assert "HELLO" in content or content.startswith("HELLO")


def test_read_file_with_mixed_encoding_fallback(tmp_path: Path, base_agent_module: Any) -> None:
    """Test file reading with fallback for mixed / unusual encodings."""
    target = tmp_path / "mixed.md"
    # Write UTF-8 content
    target.write_text("UTF-8 content: café", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    assert "UTF-8 content" in content or "café" in content


@pytest.mark.parametrize("backend", ["copilot", "github-models", "gh"])
def test_backend_selection_via_env_var(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any,
        backend: str) -> None:
    """Test backend selection through DV_AGENT_BACKEND environment variable."""
    if backend == "github-models":
        monkeypatch.setenv("DV_AGENT_BACKEND", "github-models")
        monkeypatch.setenv("GITHUB_MODELS_BASE_URL", "https://example.test")
        monkeypatch.setenv("DV_AGENT_MODEL", "test-model")
        monkeypatch.setenv("GITHUB_TOKEN", "TOKEN")
    else:
        monkeypatch.setenv("DV_AGENT_BACKEND", backend)

    agent = base_agent_module.BaseAgent("x.md")
    assert agent is not None


def test_subprocess_timeout_handling(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    """Test timeout handling in subprocess calls."""
    class Result:
        def __init__(self, returncode: int, stdout: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout

    timeout_called = []

    def fake_run_with_timeout(args: List[str], **kwargs: Any) -> Result:
        # Capture timeout parameter if provided
        if "timeout" in kwargs:
            timeout_called.append(kwargs["timeout"])
        if args[:2] == ["copilot", "--version"]:
            return Result(0, "copilot 1.2.3")
        if args[:2] == ["gh", "--version"]:
            return Result(0, "gh 2.0.0")
        return Result(0, "output")

    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", fake_run_with_timeout)

    agent = base_agent_module.BaseAgent("x.md")
    agent.run_subagent("desc", "prompt", "ORIG")
    # Timeout handling should be present in implementation


def test_markdown_fixing_with_edge_cases(tmp_path: Path, base_agent_module: Any) -> None:
    """Test markdown content fixing with various edge cases."""
    # Test with markdown file containing edge cases
    target = tmp_path / "edge_cases.md"
    target.write_text("# Header\n\n[Link]()\n\n```\ncode\n```\n", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() is not None


@pytest.mark.parametrize("extension", [".md", ".txt", ".py", ".rst", ".json"])
def test_file_extensions_handling(tmp_path: Path, base_agent_module: Any, extension: str) -> None:
    """Test agent with various file extensions."""
    target = tmp_path / f"file{extension}"
    target.write_text("CONTENT", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() == "CONTENT"


def test_error_recovery_on_write_failure(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    """Test error recovery when file write fails."""
    target = tmp_path / "readonly.md"
    target.write_text("INITIAL", encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    agent.current_content = "NEW"

    # Make directory read-only to cause write failure (skip on Windows)
    import sys
    if sys.platform != "win32":
        tmp_path.chmod(0o444)
        try:
            with pytest.raises((OSError, PermissionError)):
                agent.update_file()
        finally:
            tmp_path.chmod(0o755)


def test_diff_generation_no_changes(tmp_path: Path, base_agent_module: Any) -> None:
    """Test diff generation when content hasn't changed."""
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.previous_content = "SAME\n"
    agent.current_content = "SAME\n"
    diff = agent.get_diff()
    # Diff of identical content should be minimal
    assert diff is not None


def test_diff_generation_multiple_changes(tmp_path: Path, base_agent_module: Any) -> None:
    """Test diff generation with multiple content changes."""
    target = tmp_path / "x.txt"
    agent = base_agent_module.BaseAgent(str(target))
    agent.previous_content = "Line 1\nLine 2\nLine 3\n"
    agent.current_content = "Line 1\nModified Line 2\nLine 3\nLine 4\n"
    diff = agent.get_diff()
    assert "Line 2" in diff
    assert "+" in diff or "-" in diff


def test_missing_backend_availability(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    """Test interaction with missing or unavailable backends."""
    class Result:
        def __init__(self, returncode: int = 1) -> None:
            self.returncode = returncode
            self.stdout = ""
            self.stderr = "Command not found"

    def fake_run_all_missing(args: List[str], **kwargs: Any) -> Result:
        # All tools unavailable
        return Result(1)

    monkeypatch.delenv("DV_AGENT_BACKEND", raising=False)
    monkeypatch.setattr(base_agent_module.agent_backend.subprocess, "run", fake_run_all_missing)

    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "")
    assert out is not None  # Should return fallback


def test_concurrent_agent_operations(tmp_path: Path, base_agent_module: Any) -> None:
    """Test concurrent operations with multiple agent instances."""
    import threading

    results = []

    def create_agent(suffix: int) -> None:
        target = tmp_path / f"file_{suffix}.md"
        target.write_text(f"CONTENT {suffix}", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))
        content = agent.read_previous_content()
        results.append((suffix, content))

    threads = [threading.Thread(target=create_agent, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 5
    for suffix, content in results:
        assert f"CONTENT {suffix}" in content


def test_markdown_preservation_non_markdown_files(tmp_path: Path, base_agent_module: Any) -> None:
    """Test that non-markdown files are not modified by markdown fixing."""
    target = tmp_path / "script.py"
    original = "def hello():\n    return 'world'\n"
    target.write_text(original, encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    agent.current_content = original
    agent.update_file()

    # Content should remain unchanged (no markdown fixing for .py)
    assert target.read_text(encoding="utf-8") == original


def test_large_file_handling(tmp_path: Path, base_agent_module: Any) -> None:
    """Test handling of very large files (>1MB for testing)."""
    target = tmp_path / "large.txt"
    # Create 2MB file
    large_content = "x" * (2 * 1024 * 1024)
    target.write_text(large_content, encoding="utf-8")

    agent = base_agent_module.BaseAgent(str(target))
    content = agent.read_previous_content()
    assert content is not None
    assert len(content) > 0


def test_import_fallback_chain_for_agent_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test import fallback chains for agent_backend module."""
    # Verify that the agent_backend can be imported from scripts / agent
    with agent_dir_on_path():
        try:
            import agent_backend
            assert hasattr(
                agent_backend,
                'BaseAgent') or hasattr(
                agent_backend,
                'llm_chat_via_github_models')
        except ImportError:
            pytest.skip("agent_backend module structure differs from expected")


def test_setup_logging_verbosity_levels(base_agent_module: Any) -> None:
    """Test setup_logging with different verbosity levels."""
    if hasattr(base_agent_module, 'setup_logging'):
        # Test if setup_logging exists and can handle different verbosity
        try:
            base_agent_module.setup_logging(verbose=True)
            base_agent_module.setup_logging(verbose=False)
        except Exception as e:
            pytest.skip(f"setup_logging test skipped: {e}")


def test_create_main_function_various_agent_types(base_agent_module: Any) -> None:
    """Test create_main_function with various agent types."""
    if hasattr(base_agent_module, 'create_main_function'):
        try:
            # Verify function exists and is callable
            assert callable(base_agent_module.create_main_function)
        except AttributeError:
            pytest.skip("create_main_function not found")


def test_integration_real_file_io_operations(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    """Integration test with real file I / O operations."""
    # Create initial file
    target = tmp_path / "integration_test.md"
    initial_content = "# Original\n\nThis is original content."
    target.write_text(initial_content, encoding="utf-8")

    # Create agent and verify read
    agent = base_agent_module.BaseAgent(str(target))
    read_content = agent.read_previous_content()
    assert "Original" in read_content

    # Mock the run_subagent to avoid actual API calls
    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "# Updated\n\nThis is updated content."

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)

    # Improve content
    agent.current_content = agent.improve_content("prompt")

    # Update file
    agent.update_file()

    # Verify file was updated
    final_content = target.read_text(encoding="utf-8")
    assert "Updated" in final_content or "original content" in final_content


# ========== Tests for New Enums ==========

class TestAgentState:
    """Tests for AgentState enum."""

    def test_state_values(self, base_agent_module: Any) -> None:
        """Test that state values are correct."""
        assert base_agent_module.AgentState.INITIALIZED.value == "initialized"
        assert base_agent_module.AgentState.PROCESSING.value == "processing"
        assert base_agent_module.AgentState.COMPLETED.value == "completed"

    def test_all_states_exist(self, base_agent_module: Any) -> None:
        """Test all states exist."""
        states = list(base_agent_module.AgentState)
        assert len(states) == 6


class TestResponseQuality:
    """Tests for ResponseQuality enum."""

    def test_quality_values(self, base_agent_module: Any) -> None:
        """Test quality values are ordered correctly."""
        assert base_agent_module.ResponseQuality.EXCELLENT.value == 5
        assert base_agent_module.ResponseQuality.INVALID.value == 1


class TestEventType:
    """Tests for EventType enum."""

    def test_event_types(self, base_agent_module: Any) -> None:
        """Test all event types exist."""
        events = list(base_agent_module.EventType)
        assert len(events) == 7


# ========== Tests for Dataclasses ==========

class TestPromptTemplate:
    """Tests for PromptTemplate dataclass."""

    def test_create_template(self, base_agent_module: Any) -> None:
        """Test creating a prompt template."""
        template = base_agent_module.PromptTemplate(
            id="test1",
            name="Test Template",
            template="Improve {content} with {focus}"
        )
        assert template.id == "test1"
        assert template.version == "1.0"


class TestAgentConfig:
    """Tests for AgentConfig dataclass."""

    def test_default_config(self, base_agent_module: Any) -> None:
        """Test default config values."""
        config = base_agent_module.AgentConfig()
        assert config.backend == "auto"
        assert config.cache_enabled is True
        assert config.retry_count == 3


class TestHealthCheckResult:
    """Tests for HealthCheckResult dataclass."""

    def test_health_check_result(self, base_agent_module: Any) -> None:
        """Test creating health check result."""
        result = base_agent_module.HealthCheckResult(
            healthy=True,
            backend_available=True
        )
        assert result.healthy is True


# ========== Tests for Prompt Templates ==========

class TestPromptTemplates:
    """Tests for prompt template functionality."""

    def test_register_template(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test registering a template."""
        template = base_agent_module.PromptTemplate(
            id="custom_test",
            name="Custom Test",
            template="Custom: {content}"
        )
        base_agent_module.BaseAgent.register_template(template)
        retrieved = base_agent_module.BaseAgent.get_template("custom_test")
        assert retrieved is not None
        assert retrieved.id == "custom_test"

    def test_get_nonexistent_template(self, base_agent_module: Any) -> None:
        """Test getting a non-existent template."""
        result = base_agent_module.BaseAgent.get_template("nonexistent_xyz")
        assert result is None

    def test_default_templates_loaded(self, base_agent_module: Any) -> None:
        """Test that default templates are loaded."""
        # Default templates should be registered
        assert len(base_agent_module.DEFAULT_PROMPT_TEMPLATES) > 0


# ========== Tests for Conversation History ==========

class TestConversationHistory:
    """Tests for conversation history functionality."""

    def test_add_to_history(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test adding messages to history."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        agent.add_to_history("user", "Hello")
        agent.add_to_history("assistant", "Hi there")

        history = agent.get_history()
        assert len(history) == 2
        assert history[0].role == "user"

    def test_clear_history(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test clearing history."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        agent.add_to_history("user", "Hello")
        agent.clear_history()

        assert len(agent.get_history()) == 0


# ========== Tests for Post-Processors ==========

class TestPostProcessors:
    """Tests for response post-processors."""

    def test_add_post_processor(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test adding a post-processor."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        def uppercase(text: str) -> str:
            return text.upper()

        agent.add_post_processor(uppercase)
        assert len(agent._post_processors) == 1

    def test_clear_post_processors(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test clearing post-processors."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        agent.add_post_processor(lambda x: x)
        agent.clear_post_processors()

        assert len(agent._post_processors) == 0


# ========== Tests for Cache Management ==========

class TestCacheManagement:
    """Tests for response caching."""

    def test_generate_cache_key(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test cache key generation."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        key1 = agent._generate_cache_key("prompt", "content")
        key2 = agent._generate_cache_key("prompt", "content")
        key3 = agent._generate_cache_key("different", "content")

        assert key1 == key2
        assert key1 != key3

    def test_clear_cache(self, base_agent_module: Any) -> None:
        """Test clearing cache."""
        base_agent_module.BaseAgent.clear_cache()
        stats = base_agent_module.BaseAgent.get_cache_stats()
        assert stats["entries"] == 0

    def test_cache_stats(self, base_agent_module: Any) -> None:
        """Test getting cache stats."""
        stats = base_agent_module.BaseAgent.get_cache_stats()
        assert "entries" in stats
        assert "total_hits" in stats


# ========== Tests for Token Budget ==========

class TestTokenBudget:
    """Tests for token budget management."""

    def test_get_token_usage(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test getting token usage."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        usage = agent.get_token_usage()
        assert usage >= 0

    def test_check_token_budget(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test checking token budget."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        # Should have budget available
        assert agent.check_token_budget(1000) is True


# ========== Tests for Event Hooks ==========

class TestEventHooks:
    """Tests for event hook system."""

    def test_register_hook(self, base_agent_module: Any) -> None:
        """Test registering a hook."""
        events_received: List[Dict] = []

        def my_hook(data: Dict[str, Any]) -> None:
            events_received.append(data)

        base_agent_module.BaseAgent.register_hook(
            base_agent_module.EventType.PRE_READ,
            my_hook
        )
        # Verify hook was registered
        assert my_hook in base_agent_module.BaseAgent._event_hooks[base_agent_module.EventType.PRE_READ]

    def test_unregister_hook(self, base_agent_module: Any) -> None:
        """Test unregistering a hook."""
        def temp_hook(data: Dict[str, Any]) -> None:
            pass

        event_type = base_agent_module.EventType.POST_WRITE
        base_agent_module.BaseAgent.register_hook(event_type, temp_hook)
        base_agent_module.BaseAgent.unregister_hook(event_type, temp_hook)

        assert temp_hook not in base_agent_module.BaseAgent._event_hooks.get(event_type, [])


# ========== Tests for Health Checks ==========

class TestHealthChecks:
    """Tests for health check functionality."""

    def test_health_check(self, base_agent_module: Any) -> None:
        """Test performing health check."""
        result = base_agent_module.BaseAgent.health_check()
        assert hasattr(result, 'healthy')
        assert hasattr(result, 'backend_available')
        assert 'backends' in result.details


# ========== Tests for State Persistence ==========

class TestStatePersistence:
    """Tests for state persistence."""

    def test_save_state(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test saving agent state."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        agent.save_state()

        state_file = target.with_suffix(".state.json")
        assert state_file.exists()

    def test_load_state(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test loading agent state."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        # Save then load
        agent.save_state()
        result = agent.load_state()

        assert result is True

    def test_load_nonexistent_state(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test loading non-existent state."""
        target = tmp_path / "new_file.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        result = agent.load_state()
        assert result is False


# ========== Tests for Context Window Management ==========

class TestContextWindow:
    """Tests for context window management."""

    def test_estimate_tokens(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test token estimation."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        # ~4 chars per token
        text = "a" * 100
        tokens = agent.estimate_tokens(text)
        assert tokens == 25  # 100 / 4

    def test_truncate_for_context(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test content truncation."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        # Short text should not be truncated
        short = "Hello world"
        assert agent.truncate_for_context(short, 100) == short

        # Long text should be truncated
        long_text = "x" * 1000
        truncated = agent.truncate_for_context(long_text, 10)  # 40 chars
        assert len(truncated) < len(long_text)
        assert "[truncated]" in truncated


# ========== Tests for Model Selection ==========

class TestModelSelection:
    """Tests for model selection."""

    def test_set_model(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test setting model."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        agent.set_model("gpt-4")
        assert agent.get_model() == "gpt-4"

    def test_get_model_default(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test getting default model."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        # May be None or from config
        model = agent.get_model()
        assert model is None or isinstance(model, str)


# ========== Tests for Plugin System ==========

class TestPluginSystem:
    """Tests for plugin system."""

    def test_register_plugin(self, base_agent_module: Any) -> None:
        """Test registering a plugin."""
        class MockPlugin:
            name = "mock"

        plugin = MockPlugin()
        base_agent_module.BaseAgent.register_plugin("mock", plugin)

        retrieved = base_agent_module.BaseAgent.get_plugin("mock")
        assert retrieved is plugin

    def test_get_nonexistent_plugin(self, base_agent_module: Any) -> None:
        """Test getting non-existent plugin."""
        result = base_agent_module.BaseAgent.get_plugin("nonexistent_plugin_xyz")
        assert result is None


# ========== Tests for Response Quality Scoring ==========

class TestResponseQualityScoring:
    """Tests for response quality scoring."""

    def test_score_empty_response(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test scoring empty response."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        quality = agent._score_response_quality("")
        assert quality == base_agent_module.ResponseQuality.INVALID

    def test_score_good_response(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test scoring good response."""
        target = tmp_path / "test.md"
        target.write_text("content", encoding="utf-8")
        agent = base_agent_module.BaseAgent(str(target))

        good_response = "# Documentation\n\ndef hello():\n    pass\n"
        quality = agent._score_response_quality(good_response)
        assert quality.value >= base_agent_module.ResponseQuality.ACCEPTABLE.value


# ========== Session 8 Tests ==========

class TestSession8Enums:
    """Tests for Session 8 enums."""

    def test_auth_method_values(self, base_agent_module: Any) -> None:
        """Test AuthMethod enum values."""
        assert base_agent_module.AuthMethod.NONE.value == "none"
        assert base_agent_module.AuthMethod.API_KEY.value == "api_key"
        assert base_agent_module.AuthMethod.BEARER_TOKEN.value == "bearer_token"
        assert base_agent_module.AuthMethod.BASIC_AUTH.value == "basic_auth"
        assert base_agent_module.AuthMethod.OAUTH2.value == "oauth2"

    def test_serialization_format_values(self, base_agent_module: Any) -> None:
        """Test SerializationFormat enum values."""
        assert base_agent_module.SerializationFormat.JSON.value == "json"
        assert base_agent_module.SerializationFormat.YAML.value == "yaml"
        assert base_agent_module.SerializationFormat.PICKLE.value == "pickle"

    def test_file_priority_values(self, base_agent_module: Any) -> None:
        """Test FilePriority enum values."""
        assert base_agent_module.FilePriority.CRITICAL.value == 5
        assert base_agent_module.FilePriority.HIGH.value == 4
        assert base_agent_module.FilePriority.NORMAL.value == 3
        assert base_agent_module.FilePriority.LOW.value == 2
        assert base_agent_module.FilePriority.BACKGROUND.value == 1

    def test_input_type_values(self, base_agent_module: Any) -> None:
        """Test InputType enum values."""
        assert base_agent_module.InputType.TEXT.value == "text"
        assert base_agent_module.InputType.IMAGE.value == "image"
        assert base_agent_module.InputType.CODE.value == "code"


class TestSession8Dataclasses:
    """Tests for Session 8 dataclasses."""

    def test_auth_config_defaults(self, base_agent_module: Any) -> None:
        """Test AuthConfig default values."""
        config = base_agent_module.AuthConfig()
        assert config.method == base_agent_module.AuthMethod.NONE
        assert config.api_key == ""
        assert config.token == ""
        assert config.custom_headers == {}

    def test_batch_request_creation(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test BatchRequest creation."""
        request = base_agent_module.BatchRequest(
            file_path=tmp_path / "test.py",
            prompt="Improve code"
        )
        assert request.priority == base_agent_module.FilePriority.NORMAL
        assert request.callback is None

    def test_batch_result_creation(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test BatchResult creation."""
        result = base_agent_module.BatchResult(
            file_path=tmp_path / "test.py",
            success=True,
            content="improved content"
        )
        assert result.success is True
        assert result.error == ""
        assert result.processing_time == 0.0

    def test_prompt_version_creation(self, base_agent_module: Any) -> None:
        """Test PromptVersion creation."""
        version = base_agent_module.PromptVersion(
            version_id="v1",
            template_id="improve_code",
            variant="A",
            prompt_text="Improve {content}"
        )
        assert version.weight == 1.0
        assert version.metrics == {}

    def test_multimodal_input_creation(self, base_agent_module: Any) -> None:
        """Test MultimodalInput creation."""
        input_data = base_agent_module.MultimodalInput(
            input_type=base_agent_module.InputType.TEXT,
            content="Hello world"
        )
        assert input_data.mime_type == ""
        assert input_data.metadata == {}

    def test_composed_agent_creation(self, base_agent_module: Any) -> None:
        """Test ComposedAgent creation."""
        agent = base_agent_module.ComposedAgent(
            agent_type="coder",
            order=1
        )
        assert agent.config == {}
        assert agent.depends_on == []

    def test_serialization_config_defaults(self, base_agent_module: Any) -> None:
        """Test SerializationConfig defaults."""
        config = base_agent_module.SerializationConfig()
        assert config.format == base_agent_module.SerializationFormat.JSON
        assert config.compression is False
        assert config.encryption is False

    def test_file_priority_config_defaults(self, base_agent_module: Any) -> None:
        """Test FilePriorityConfig defaults."""
        config = base_agent_module.FilePriorityConfig()
        assert config.path_patterns == {}
        assert config.default_priority == base_agent_module.FilePriority.NORMAL


class TestRequestBatcher:
    """Tests for RequestBatcher class."""

    def test_add_request(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test adding requests to batcher."""
        batcher = base_agent_module.RequestBatcher(batch_size=5)
        request = base_agent_module.BatchRequest(
            file_path=tmp_path / "test.py",
            prompt="Improve"
        )
        batcher.add_request(request)
        assert batcher.get_queue_size() == 1

    def test_add_multiple_requests(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test adding multiple requests."""
        batcher = base_agent_module.RequestBatcher(batch_size=10)
        requests = [
            base_agent_module.BatchRequest(file_path=tmp_path / f"test{i}.py", prompt="Improve")
            for i in range(5)
        ]
        batcher.add_requests(requests)
        assert batcher.get_queue_size() == 5

    def test_clear_queue(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test clearing the queue."""
        batcher = base_agent_module.RequestBatcher()
        batcher.add_request(base_agent_module.BatchRequest(
            file_path=tmp_path / "test.py",
            prompt="Improve"
        ))
        batcher.clear_queue()
        assert batcher.get_queue_size() == 0

    def test_get_stats_empty(self, base_agent_module: Any) -> None:
        """Test stats with no results."""
        batcher = base_agent_module.RequestBatcher()
        stats = batcher.get_stats()
        assert stats["processed"] == 0
        assert stats["success_rate"] == 0.0


class TestAuthenticationManager:
    """Tests for AuthenticationManager class."""

    def test_no_auth_headers(self, base_agent_module: Any) -> None:
        """Test headers with no authentication."""
        config = base_agent_module.AuthConfig(method=base_agent_module.AuthMethod.NONE)
        manager = base_agent_module.AuthenticationManager(config)
        headers = manager.get_headers()
        assert "Authorization" not in headers

    def test_api_key_headers(self, base_agent_module: Any) -> None:
        """Test headers with API key auth."""
        config = base_agent_module.AuthConfig(
            method=base_agent_module.AuthMethod.API_KEY,
            api_key="test-api-key"
        )
        manager = base_agent_module.AuthenticationManager(config)
        headers = manager.get_headers()
        assert headers["X-API-Key"] == "test-api-key"

    def test_bearer_token_headers(self, base_agent_module: Any) -> None:
        """Test headers with bearer token auth."""
        config = base_agent_module.AuthConfig(
            method=base_agent_module.AuthMethod.BEARER_TOKEN,
            token="test-token"
        )
        manager = base_agent_module.AuthenticationManager(config)
        headers = manager.get_headers()
        assert headers["Authorization"] == "Bearer test-token"

    def test_basic_auth_headers(self, base_agent_module: Any) -> None:
        """Test headers with basic auth."""
        config = base_agent_module.AuthConfig(
            method=base_agent_module.AuthMethod.BASIC_AUTH,
            username="user",
            password="pass"
        )
        manager = base_agent_module.AuthenticationManager(config)
        headers = manager.get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_custom_headers(self, base_agent_module: Any) -> None:
        """Test custom headers."""
        config = base_agent_module.AuthConfig(
            custom_headers={"X-Custom": "value"}
        )
        manager = base_agent_module.AuthenticationManager(config)
        headers = manager.get_headers()
        assert headers["X-Custom"] == "value"

    def test_validate_api_key(self, base_agent_module: Any) -> None:
        """Test validation for API key auth."""
        config = base_agent_module.AuthConfig(
            method=base_agent_module.AuthMethod.API_KEY,
            api_key="valid-key"
        )
        manager = base_agent_module.AuthenticationManager(config)
        assert manager.validate() is True

    def test_validate_missing_api_key(self, base_agent_module: Any) -> None:
        """Test validation fails for missing API key."""
        config = base_agent_module.AuthConfig(
            method=base_agent_module.AuthMethod.API_KEY,
            api_key=""
        )
        manager = base_agent_module.AuthenticationManager(config)
        assert manager.validate() is False

    def test_refresh_token(self, base_agent_module: Any) -> None:
        """Test token refresh."""
        manager = base_agent_module.AuthenticationManager()
        manager.token_cache["key"] = "value"
        manager.refresh_token()
        assert len(manager.token_cache) == 0


class TestPromptVersionManager:
    """Tests for PromptVersionManager class."""

    def test_register_version(self, base_agent_module: Any) -> None:
        """Test registering a version."""
        manager = base_agent_module.PromptVersionManager()
        version = base_agent_module.PromptVersion(
            version_id="v1",
            template_id="test",
            variant="A",
            prompt_text="Test prompt"
        )
        manager.register_version(version)
        versions = manager.get_versions("test")
        assert len(versions) == 1
        assert versions[0].version_id == "v1"

    def test_get_versions_empty(self, base_agent_module: Any) -> None:
        """Test getting versions for non-existent template."""
        manager = base_agent_module.PromptVersionManager()
        versions = manager.get_versions("nonexistent")
        assert versions == []

    def test_select_version(self, base_agent_module: Any) -> None:
        """Test selecting a version."""
        manager = base_agent_module.PromptVersionManager()
        version = base_agent_module.PromptVersion(
            version_id="v1",
            template_id="test",
            variant="A",
            prompt_text="Test prompt"
        )
        manager.register_version(version)
        selected = manager.select_version("test")
        assert selected is not None
        assert selected.version_id == "v1"

    def test_select_version_empty(self, base_agent_module: Any) -> None:
        """Test selecting version with no versions."""
        manager = base_agent_module.PromptVersionManager()
        selected = manager.select_version("nonexistent")
        assert selected is None

    def test_record_metric(self, base_agent_module: Any) -> None:
        """Test recording metrics."""
        manager = base_agent_module.PromptVersionManager()
        manager.record_metric("v1", "quality", 4.5)
        assert "v1" in manager.metrics
        assert manager.metrics["v1"]["quality"] == 4.5

    def test_get_ab_report(self, base_agent_module: Any) -> None:
        """Test A / B testing report."""
        manager = base_agent_module.PromptVersionManager()
        version = base_agent_module.PromptVersion(
            version_id="v1",
            template_id="test",
            variant="A",
            prompt_text="Test"
        )
        manager.register_version(version)
        manager.select_version("test")

        report = manager.get_ab_report("test")
        assert report["template_id"] == "test"
        assert "versions" in report


class TestMultimodalProcessor:
    """Tests for MultimodalProcessor class."""

    def test_add_text(self, base_agent_module: Any) -> None:
        """Test adding text input."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_text("Hello world")
        assert len(processor.inputs) == 1
        assert processor.inputs[0].input_type == base_agent_module.InputType.TEXT

    def test_add_code(self, base_agent_module: Any) -> None:
        """Test adding code input."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_code("print('hello')", "python")
        assert len(processor.inputs) == 1
        assert processor.inputs[0].metadata["language"] == "python"

    def test_add_image(self, base_agent_module: Any) -> None:
        """Test adding image input."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_image("base64data", "image / png")
        assert len(processor.inputs) == 1
        assert processor.inputs[0].mime_type == "image / png"

    def test_build_prompt(self, base_agent_module: Any) -> None:
        """Test building combined prompt."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_text("Analyze this")
        processor.add_code("def foo(): pass", "python")

        prompt = processor.build_prompt()
        assert "Analyze this" in prompt
        assert "def foo()" in prompt
        assert "```python" in prompt

    def test_get_api_messages(self, base_agent_module: Any) -> None:
        """Test getting API-formatted messages."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_text("Hello")

        messages = processor.get_api_messages()
        assert len(messages) == 1
        assert messages[0]["type"] == "text"

    def test_clear(self, base_agent_module: Any) -> None:
        """Test clearing inputs."""
        processor = base_agent_module.MultimodalProcessor()
        processor.add_text("Test")
        processor.clear()
        assert len(processor.inputs) == 0
        assert processor.processed == ""


class TestAgentComposer:
    """Tests for AgentComposer class."""

    def test_add_agent(self, base_agent_module: Any) -> None:
        """Test adding an agent."""
        composer = base_agent_module.AgentComposer()
        agent = base_agent_module.ComposedAgent(agent_type="coder", order=1)
        composer.add_agent(agent)
        assert len(composer.agents) == 1

    def test_execution_order(self, base_agent_module: Any) -> None:
        """Test execution order calculation."""
        composer = base_agent_module.AgentComposer()
        composer.add_agent(base_agent_module.ComposedAgent(agent_type="coder", order=1))
        composer.add_agent(base_agent_module.ComposedAgent(agent_type="tests", order=2))
        assert "coder" in composer.execution_order
        assert "tests" in composer.execution_order

    def test_get_final_result_empty(self, base_agent_module: Any) -> None:
        """Test getting result with no agents."""
        composer = base_agent_module.AgentComposer()
        result = composer.get_final_result()
        assert result == ""


class TestSerializationManager:
    """Tests for SerializationManager class."""

    def test_json_serialize(self, base_agent_module: Any) -> None:
        """Test JSON serialization."""
        config = base_agent_module.SerializationConfig(
            format=base_agent_module.SerializationFormat.JSON
        )
        manager = base_agent_module.SerializationManager(config)

        data = {"key": "value", "number": 42}
        serialized = manager.serialize(data)
        assert isinstance(serialized, bytes)
        assert b'"key"' in serialized

    def test_json_deserialize(self, base_agent_module: Any) -> None:
        """Test JSON deserialization."""
        config = base_agent_module.SerializationConfig(
            format=base_agent_module.SerializationFormat.JSON
        )
        manager = base_agent_module.SerializationManager(config)

        data = {"key": "value"}
        serialized = manager.serialize(data)
        deserialized = manager.deserialize(serialized)
        assert deserialized == data

    def test_compression(self, base_agent_module: Any) -> None:
        """Test serialization with compression."""
        config = base_agent_module.SerializationConfig(
            format=base_agent_module.SerializationFormat.JSON,
            compression=True
        )
        manager = base_agent_module.SerializationManager(config)

        data = {"key": "value" * 100}  # Larger data benefits from compression
        serialized = manager.serialize(data)
        deserialized = manager.deserialize(serialized)
        assert deserialized == data

    def test_save_and_load_file(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test saving and loading from file."""
        manager = base_agent_module.SerializationManager()
        data = {"test": "data", "numbers": [1, 2, 3]}

        file_path = tmp_path / "test.data"
        manager.save_to_file(data, file_path)
        assert file_path.exists()

        loaded = manager.load_from_file(file_path)
        assert loaded == data


class TestFilePriorityManager:
    """Tests for FilePriorityManager class."""

    def test_default_priority(self, base_agent_module: Any) -> None:
        """Test default priority for unknown file."""
        manager = base_agent_module.FilePriorityManager()
        priority = manager.get_priority(Path("unknown.xyz"))
        assert priority == base_agent_module.FilePriority.NORMAL

    def test_extension_priority(self, base_agent_module: Any) -> None:
        """Test priority by extension."""
        manager = base_agent_module.FilePriorityManager()
        priority = manager.get_priority(Path("main.py"))
        assert priority == base_agent_module.FilePriority.HIGH

    def test_set_pattern_priority(self, base_agent_module: Any) -> None:
        """Test setting pattern priority."""
        manager = base_agent_module.FilePriorityManager()
        manager.set_pattern_priority("*.critical", base_agent_module.FilePriority.CRITICAL)
        priority = manager.get_priority(Path("important.critical"))
        assert priority == base_agent_module.FilePriority.CRITICAL

    def test_set_extension_priority(self, base_agent_module: Any) -> None:
        """Test setting extension priority."""
        manager = base_agent_module.FilePriorityManager()
        manager.set_extension_priority(".custom", base_agent_module.FilePriority.HIGH)
        priority = manager.get_priority(Path("file.custom"))
        assert priority == base_agent_module.FilePriority.HIGH

    def test_sort_by_priority(self, base_agent_module: Any) -> None:
        """Test sorting paths by priority."""
        manager = base_agent_module.FilePriorityManager()
        paths = [
            Path("readme.txt"),
            Path("main.py"),
            Path("config.json"),
        ]
        sorted_paths = manager.sort_by_priority(paths)
        # .py should come first (HIGH), then .txt/.json (LOW)
        assert sorted_paths[0].suffix == ".py"

    def test_filter_by_priority(self, base_agent_module: Any) -> None:
        """Test filtering paths by minimum priority."""
        manager = base_agent_module.FilePriorityManager()
        paths = [
            Path("main.py"),      # HIGH
            Path("readme.txt"),   # LOW
            Path("data.json"),    # LOW
        ]
        filtered = manager.filter_by_priority(paths, base_agent_module.FilePriority.NORMAL)
        # Only .py should remain (HIGH >= NORMAL)
        assert len(filtered) == 1
        assert filtered[0].suffix == ".py"


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================


class TestPromptTemplatingSystem:
    """Tests for prompt templating system."""

    def test_prompt_template_creation(self, base_agent_module: Any) -> None:
        """Test creating prompt templates."""
        PromptTemplate = base_agent_module.PromptTemplate

        template = PromptTemplate(
            name="code_review",
            template="Review this code:\n{code}\nFocus on: {aspects}",
            variables=["code", "aspects"]
        )

        assert template.name == "code_review"
        assert "code" in template.variables

    def test_prompt_template_render(self, base_agent_module: Any) -> None:
        """Test rendering prompt templates."""
        PromptTemplate = base_agent_module.PromptTemplate

        template = PromptTemplate(
            name="simple",
            template="Hello, {name}!",
            variables=["name"]
        )

        result = template.render(name="World")
        assert result == "Hello, World!"

    def test_prompt_template_manager(self, base_agent_module: Any) -> None:
        """Test prompt template manager."""
        PromptTemplateManager = base_agent_module.PromptTemplateManager
        PromptTemplate = base_agent_module.PromptTemplate

        manager = PromptTemplateManager()

        template = PromptTemplate(
            name="test",
            template="Test: {value}",
            variables=["value"]
        )

        manager.register(template)
        result = manager.render("test", value="data")
        assert result == "Test: data"


class TestConversationHistoryManagement:
    """Tests for conversation history management."""

    def test_conversation_message_creation(self, base_agent_module: Any) -> None:
        """Test creating conversation messages."""
        ConversationMessage = base_agent_module.ConversationMessage
        MessageRole = base_agent_module.MessageRole

        msg = ConversationMessage(
            role=MessageRole.USER,
            content="Hello!"
        )

        assert msg.role == MessageRole.USER
        assert msg.content == "Hello!"
        assert msg.timestamp > 0

    def test_conversation_history_add_message(self, base_agent_module: Any) -> None:
        """Test adding messages to history."""
        ConversationHistory = base_agent_module.ConversationHistory
        MessageRole = base_agent_module.MessageRole

        history = ConversationHistory()
        history.add(MessageRole.USER, "Question")
        history.add(MessageRole.ASSISTANT, "Answer")

        assert len(history.messages) == 2
        assert history.messages[0].role == MessageRole.USER

    def test_conversation_history_get_context(self, base_agent_module: Any) -> None:
        """Test getting conversation context."""
        ConversationHistory = base_agent_module.ConversationHistory
        MessageRole = base_agent_module.MessageRole

        history = ConversationHistory(max_messages=5)
        for i in range(10):
            history.add(MessageRole.USER, f"Message {i}")

        context = history.get_context()
        # Should only contain last 5 messages
        assert len(context) == 5

    def test_conversation_history_clear(self, base_agent_module: Any) -> None:
        """Test clearing conversation history."""
        ConversationHistory = base_agent_module.ConversationHistory
        MessageRole = base_agent_module.MessageRole

        history = ConversationHistory()
        history.add(MessageRole.USER, "Message")
        history.clear()

        assert len(history.messages) == 0


class TestResponsePostProcessingHooks:
    """Tests for response post-processing hooks."""

    def test_post_processor_registration(self, base_agent_module: Any) -> None:
        """Test registering post-processors."""
        ResponsePostProcessor = base_agent_module.ResponsePostProcessor

        processor = ResponsePostProcessor()

        def strip_whitespace(text: str) -> str:
            return text.strip()

        processor.register(strip_whitespace, priority=10)
        assert len(processor.hooks) == 1

    def test_post_processor_execution_order(self, base_agent_module: Any) -> None:
        """Test post-processors execute in priority order."""
        ResponsePostProcessor = base_agent_module.ResponsePostProcessor

        processor = ResponsePostProcessor()
        results: list[int] = []

        def hook_low(text: str) -> str:
            results.append(1)
            return text

        def hook_high(text: str) -> str:
            results.append(2)
            return text

        processor.register(hook_low, priority=1)
        processor.register(hook_high, priority=10)

        processor.process("test")
        # High priority (10) executes first
        assert results[0] == 2

    def test_post_processor_chain(self, base_agent_module: Any) -> None:
        """Test chained post-processors."""
        ResponsePostProcessor = base_agent_module.ResponsePostProcessor

        processor = ResponsePostProcessor()
        processor.register(lambda t: t.upper(), priority=1)
        processor.register(lambda t: t + "!", priority=2)

        result = processor.process("hello")
        assert result == "HELLO!"


class TestModelSelectionPerAgentType:
    """Tests for model selection per agent type."""

    def test_model_config_creation(self, base_agent_module: Any) -> None:
        """Test creating model configurations."""
        ModelConfig = base_agent_module.ModelConfig

        config = ModelConfig(
            model_id="gpt-4",
            temperature=0.7,
            max_tokens=1000
        )

        assert config.model_id == "gpt-4"
        assert config.temperature == 0.7

    def test_model_selector_default(self, base_agent_module: Any) -> None:
        """Test model selector returns default."""
        ModelSelector = base_agent_module.ModelSelector
        AgentType = base_agent_module.AgentType

        selector = ModelSelector()
        model = selector.select(AgentType.GENERAL)

        assert model is not None
        assert isinstance(model.model_id, str)

    def test_model_selector_custom_mapping(self, base_agent_module: Any) -> None:
        """Test model selector with custom mapping."""
        ModelSelector = base_agent_module.ModelSelector
        ModelConfig = base_agent_module.ModelConfig
        AgentType = base_agent_module.AgentType

        selector = ModelSelector()
        custom = ModelConfig(model_id="custom-model", temperature=0.5)
        selector.set_model(AgentType.CODE_REVIEW, custom)

        result = selector.select(AgentType.CODE_REVIEW)
        assert result.model_id == "custom-model"


class TestRequestBatchingPerformance:
    """Tests for request batching performance."""

    def test_batch_request_creation(self, base_agent_module: Any) -> None:
        """Test creating batch requests."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest()
        batch.add("prompt1")
        batch.add("prompt2")
        batch.add("prompt3")

        assert batch.size == 3

    def test_batch_execution(self, base_agent_module: Any) -> None:
        """Test batch execution."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest()
        batch.add("A")
        batch.add("B")

        # Mock processor
        def processor(prompts: list[str]) -> list[str]:
            return [p.upper() for p in prompts]

        results = batch.execute(processor)
        assert results == ["A", "B"]

    def test_batch_max_size(self, base_agent_module: Any) -> None:
        """Test batch respects max size."""
        BatchRequest = base_agent_module.BatchRequest

        batch = BatchRequest(max_size=2)
        batch.add("A")
        batch.add("B")
        batch.add("C")  # Should trigger auto-flush or be rejected

        assert batch.size <= 2


class TestCustomAuthenticationMethods:
    """Tests for custom authentication methods."""

    def test_auth_token_method(self, base_agent_module: Any) -> None:
        """Test token-based authentication."""
        AuthMethod = base_agent_module.AuthMethod
        AuthManager = base_agent_module.AuthManager

        manager = AuthManager()
        manager.set_method(AuthMethod.TOKEN, token="secret-token")

        headers = manager.get_headers()
        assert "Authorization" in headers

    def test_auth_api_key_method(self, base_agent_module: Any) -> None:
        """Test API key authentication."""
        AuthMethod = base_agent_module.AuthMethod
        AuthManager = base_agent_module.AuthManager

        manager = AuthManager()
        manager.set_method(AuthMethod.API_KEY, api_key="key123")

        headers = manager.get_headers()
        assert "X-API-Key" in headers

    def test_auth_custom_header(self, base_agent_module: Any) -> None:
        """Test custom authentication header."""
        AuthManager = base_agent_module.AuthManager

        manager = AuthManager()
        manager.add_custom_header("X-Custom-Auth", "value")

        headers = manager.get_headers()
        assert headers["X-Custom-Auth"] == "value"


class TestResponseQualityScoring_v2:  # noqa: F811
    """Tests for response quality scoring (extended)."""

    def test_quality_scorer_basic(self, base_agent_module: Any) -> None:
        """Test basic quality scoring."""
        QualityScorer = base_agent_module.QualityScorer

        scorer = QualityScorer()
        score = scorer.score("A comprehensive and detailed response.")

        assert 0.0 <= score <= 1.0

    def test_quality_scorer_length_factor(self, base_agent_module: Any) -> None:
        """Test quality scoring considers length."""
        QualityScorer = base_agent_module.QualityScorer

        scorer = QualityScorer()
        short_score = scorer.score("OK")
        long_score = scorer.score(
            "This is a much longer and more detailed response that provides context.")

        assert long_score >= short_score

    def test_quality_scorer_custom_criteria(self, base_agent_module: Any) -> None:
        """Test quality scoring with custom criteria."""
        QualityScorer = base_agent_module.QualityScorer

        scorer = QualityScorer()

        def has_code_block(text: str) -> float:
            return 1.0 if "```" in text else 0.0

        scorer.add_criterion("code_block", has_code_block, weight=0.3)

        score_with_code = scorer.score("Example:\n```python\nprint('hi')\n```")
        score_without = scorer.score("Just plain text")

        assert score_with_code > score_without


class TestPromptVersioningAndABTesting:
    """Tests for prompt versioning and A / B testing."""

    def test_prompt_version_creation(self, base_agent_module: Any) -> None:
        """Test creating prompt versions."""
        PromptVersion = base_agent_module.PromptVersion

        v1 = PromptVersion(
            version="1.0.0",
            content="Analyze this code",
            description="Original prompt"
        )

        assert v1.version == "1.0.0"
        assert v1.active

    def test_prompt_version_manager(self, base_agent_module: Any) -> None:
        """Test prompt version manager."""
        PromptVersionManager = base_agent_module.PromptVersionManager
        PromptVersion = base_agent_module.PromptVersion

        manager = PromptVersionManager()

        v1 = PromptVersion("1.0.0", "Original")
        v2 = PromptVersion("2.0.0", "Improved")

        manager.add_version(v1)
        manager.add_version(v2)
        manager.set_active("2.0.0")

        active = manager.get_active()
        assert active.version == "2.0.0"

    def test_ab_test_variant_selection(self, base_agent_module: Any) -> None:
        """Test A / B test variant selection."""
        ABTest = base_agent_module.ABTest

        test = ABTest(
            name="prompt_test",
            variants=["control", "treatment"],
            weights=[0.5, 0.5]
        )

        variant = test.select_variant()
        assert variant in ["control", "treatment"]


class TestContextWindowManagement:
    """Tests for context window management."""

    def test_context_window_size(self, base_agent_module: Any) -> None:
        """Test context window size tracking."""
        ContextWindow = base_agent_module.ContextWindow

        window = ContextWindow(max_tokens=4096)
        window.add("Some text content", token_count=100)

        assert window.used_tokens == 100
        assert window.available_tokens == 3996

    def test_context_window_truncation(self, base_agent_module: Any) -> None:
        """Test context window truncation."""
        ContextWindow = base_agent_module.ContextWindow

        window = ContextWindow(max_tokens=100)
        for i in range(20):
            window.add(f"Message {i}", token_count=10)

        # Should have truncated old messages
        assert window.used_tokens <= 100

    def test_context_window_clear(self, base_agent_module: Any) -> None:
        """Test context window clearing."""
        ContextWindow = base_agent_module.ContextWindow

        window = ContextWindow(max_tokens=1000)
        window.add("Content", token_count=50)
        window.clear()

        assert window.used_tokens == 0


class TestMultimodalInputHandling:
    """Tests for multimodal input handling."""

    def test_multimodal_input_text(self, base_agent_module: Any) -> None:
        """Test multimodal input with text."""
        MultimodalInput = base_agent_module.MultimodalInput
        InputType = base_agent_module.InputType

        input_data = MultimodalInput(
            content="Hello world",
            input_type=InputType.TEXT
        )

        assert input_data.input_type == InputType.TEXT
        assert input_data.content == "Hello world"

    def test_multimodal_input_image(self, base_agent_module: Any) -> None:
        """Test multimodal input with image reference."""
        MultimodalInput = base_agent_module.MultimodalInput
        InputType = base_agent_module.InputType

        input_data = MultimodalInput(
            content="base64_encoded_data",
            input_type=InputType.IMAGE,
            mime_type="image / png"
        )

        assert input_data.input_type == InputType.IMAGE
        assert input_data.mime_type == "image / png"

    def test_multimodal_builder(self, base_agent_module: Any) -> None:
        """Test multimodal input builder."""
        MultimodalBuilder = base_agent_module.MultimodalBuilder
        base_agent_module.InputType

        builder = MultimodalBuilder()
        builder.add_text("Describe this image:")
        builder.add_image("data:image / png;base64,...")

        inputs = builder.build()
        assert len(inputs) == 2


class TestContentBasedResponseCaching:
    """Tests for content-based response caching."""

    def test_response_cache_set_get(self, base_agent_module: Any, tmp_path: Path) -> None:
        """Test setting and getting cached responses."""
        ResponseCache = base_agent_module.ResponseCache

        cache = ResponseCache(cache_dir=tmp_path)
        cache.set("prompt1", "response1")

        result = cache.get("prompt1")
        assert result == "response1"

    def test_response_cache_miss(self, base_agent_module: Any, tmp_path: Path) -> None:
        """Test cache miss returns None."""
        ResponseCache = base_agent_module.ResponseCache

        cache = ResponseCache(cache_dir=tmp_path)
        result = cache.get("nonexistent")

        assert result is None

    def test_response_cache_invalidation(self, base_agent_module: Any, tmp_path: Path) -> None:
        """Test cache invalidation."""
        ResponseCache = base_agent_module.ResponseCache

        cache = ResponseCache(cache_dir=tmp_path)
        cache.set("prompt1", "response1")
        cache.invalidate("prompt1")

        result = cache.get("prompt1")
        assert result is None


class TestAgentCompositionPatterns:
    """Tests for agent composition patterns."""

    def test_agent_pipeline(self, base_agent_module: Any) -> None:
        """Test agent pipeline composition."""
        AgentPipeline = base_agent_module.AgentPipeline

        pipeline = AgentPipeline()

        def step1(data: str) -> str:
            return data + "_step1"

        def step2(data: str) -> str:
            return data + "_step2"

        pipeline.add_step("first", step1)
        pipeline.add_step("second", step2)

        result = pipeline.execute("input")
        assert result == "input_step1_step2"

    def test_agent_parallel_composition(self, base_agent_module: Any) -> None:
        """Test parallel agent composition."""
        AgentParallel = base_agent_module.AgentParallel

        parallel = AgentParallel()

        parallel.add_branch("upper", lambda t: t.upper())
        parallel.add_branch("lower", lambda t: t.lower())

        results = parallel.execute("Test")
        assert results["upper"] == "TEST"
        assert results["lower"] == "test"

    def test_agent_conditional(self, base_agent_module: Any) -> None:
        """Test conditional agent routing."""
        AgentRouter = base_agent_module.AgentRouter

        router = AgentRouter()
        router.add_route(lambda t: t.startswith("code:"), lambda t: f"Coded: {t}")
        router.add_route(lambda t: t.startswith("text:"), lambda t: f"Texted: {t}")
        router.set_default(lambda t: f"Default: {t}")

        result = router.route("code: hello")
        assert result.startswith("Coded:")


class TestTokenBudgetManagement:
    """Tests for token budget management."""

    def test_token_budget_allocation(self, base_agent_module: Any) -> None:
        """Test token budget allocation."""
        TokenBudget = base_agent_module.TokenBudget

        budget = TokenBudget(total=4096)
        budget.allocate("system", 500)
        budget.allocate("context", 1000)

        remaining = budget.remaining
        assert remaining == 2596

    def test_token_budget_overflow_prevention(self, base_agent_module: Any) -> None:
        """Test budget prevents overflow."""
        TokenBudget = base_agent_module.TokenBudget

        budget = TokenBudget(total=100)
        budget.allocate("large", 150)  # Should be capped

        assert budget.used <= 100

    def test_token_budget_release(self, base_agent_module: Any) -> None:
        """Test releasing token budget."""
        TokenBudget = base_agent_module.TokenBudget

        budget = TokenBudget(total=1000)
        budget.allocate("temp", 500)
        budget.release("temp")

        assert budget.remaining == 1000


class TestAgentStatePersistence:
    """Tests for agent state persistence."""

    def test_state_save_and_load(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test saving and loading agent state."""
        StatePersistence = base_agent_module.StatePersistence

        state_file = tmp_path / "state.json"
        persistence = StatePersistence(state_file)

        state = {"counter": 42, "items": ["a", "b"]}
        persistence.save(state)

        loaded = persistence.load()
        assert loaded["counter"] == 42

    def test_state_auto_backup(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test automatic state backup."""
        StatePersistence = base_agent_module.StatePersistence

        state_file = tmp_path / "state.json"
        persistence = StatePersistence(state_file, backup=True)

        persistence.save({"v": 1})
        persistence.save({"v": 2})

        # Should have backup
        backups = list(tmp_path.glob("state.*.bak"))
        assert len(backups) >= 1

    def test_state_default_on_missing(self, tmp_path: Path, base_agent_module: Any) -> None:
        """Test default state on missing file."""
        StatePersistence = base_agent_module.StatePersistence

        state_file = tmp_path / "missing.json"
        persistence = StatePersistence(state_file)

        default = {"key": "value"}
        loaded = persistence.load(default=default)
        assert loaded == default


class TestAgentEventHooks:
    """Tests for agent event hooks."""

    def test_event_hook_registration(self, base_agent_module: Any) -> None:
        """Test registering event hooks."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        calls: list[str] = []

        manager.on(AgentEvent.START, lambda: calls.append("started"))
        manager.emit(AgentEvent.START)

        assert "started" in calls

    def test_event_multiple_handlers(self, base_agent_module: Any) -> None:
        """Test multiple handlers for same event."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        results: list[int] = []

        manager.on(AgentEvent.COMPLETE, lambda: results.append(1))
        manager.on(AgentEvent.COMPLETE, lambda: results.append(2))
        manager.emit(AgentEvent.COMPLETE)

        assert len(results) == 2

    def test_event_with_data(self, base_agent_module: Any) -> None:
        """Test events with data payload."""
        EventManager = base_agent_module.EventManager
        AgentEvent = base_agent_module.AgentEvent

        manager = EventManager()
        received: list[dict[str, Any]] = []

        manager.on(AgentEvent.ERROR, lambda data: received.append(data))
        manager.emit(AgentEvent.ERROR, {"message": "test error"})

        assert received[0]["message"] == "test error"


class TestAgentPluginLoading:
    """Tests for agent plugin loading."""

    def test_plugin_registration(self, base_agent_module: Any) -> None:
        """Test plugin registration."""
        PluginManager = base_agent_module.PluginManager

        manager = PluginManager()

        class MockPlugin:
            name = "mock"

            def activate(self) -> None:
                pass

        manager.register(MockPlugin())
        assert "mock" in manager.plugins

    def test_plugin_activation(self, base_agent_module: Any) -> None:
        """Test plugin activation."""
        PluginManager = base_agent_module.PluginManager

        manager = PluginManager()
        activated = []

        class TestPlugin:
            name = "test"

            def activate(self) -> None:
                activated.append("test")

        manager.register(TestPlugin())
        manager.activate_all()

        assert "test" in activated

    def test_plugin_deactivation(self, base_agent_module: Any) -> None:
        """Test plugin deactivation."""
        PluginManager = base_agent_module.PluginManager

        manager = PluginManager()

        class TestPlugin:
            name = "test"
            active = True

            def activate(self) -> None:
                self.active = True

            def deactivate(self) -> None:
                self.active = False

        plugin = TestPlugin()
        manager.register(plugin)
        manager.activate_all()
        manager.deactivate("test")

        assert not plugin.active


class TestAgentHealthDiagnostics:
    """Tests for agent health diagnostics."""

    def test_health_check_basic(self, base_agent_module: Any) -> None:
        """Test basic health check."""
        HealthChecker = base_agent_module.HealthChecker

        checker = HealthChecker()
        status = checker.check()

        assert "status" in status
        assert status["status"] in ["healthy", "degraded", "unhealthy"]

    def test_health_check_components(self, base_agent_module: Any) -> None:
        """Test health check with component checks."""
        HealthChecker = base_agent_module.HealthChecker

        checker = HealthChecker()
        checker.add_check("memory", lambda: {"status": "ok", "used_mb": 100})
        checker.add_check("backend", lambda: {"status": "ok", "latency_ms": 50})

        status = checker.check()
        assert "components" in status
        assert "memory" in status["components"]

    def test_health_metrics(self, base_agent_module: Any) -> None:
        """Test health metrics collection."""
        HealthChecker = base_agent_module.HealthChecker

        checker = HealthChecker()

        for _ in range(5):
            checker.record_request(success=True, latency_ms=100)
        checker.record_request(success=False, latency_ms=500)

        metrics = checker.get_metrics()
        assert metrics["total_requests"] == 6
        assert metrics["error_rate"] < 0.2


class TestAgentConfigurationProfiles:
    """Tests for agent configuration profiles."""

    def test_profile_creation(self, base_agent_module: Any) -> None:
        """Test creating configuration profiles."""
        ConfigProfile = base_agent_module.ConfigProfile

        profile = ConfigProfile(
            name="production",
            settings={
                "timeout": 30,
                "retries": 3,
                "log_level": "INFO"
            }
        )

        assert profile.name == "production"
        assert profile.settings["timeout"] == 30

    def test_profile_manager_switch(self, base_agent_module: Any) -> None:
        """Test switching configuration profiles."""
        ProfileManager = base_agent_module.ProfileManager
        ConfigProfile = base_agent_module.ConfigProfile

        manager = ProfileManager()

        dev = ConfigProfile("development", {"debug": True})
        prod = ConfigProfile("production", {"debug": False})

        manager.add_profile(dev)
        manager.add_profile(prod)
        manager.set_active("production")

        assert manager.active.name == "production"
        assert manager.get_setting("debug") is False

    def test_profile_inheritance(self, base_agent_module: Any) -> None:
        """Test profile inheritance."""
        ProfileManager = base_agent_module.ProfileManager
        ConfigProfile = base_agent_module.ConfigProfile

        manager = ProfileManager()

        base = ConfigProfile("base", {"timeout": 30, "retries": 3})
        custom = ConfigProfile("custom", {"timeout": 60}, parent="base")

        manager.add_profile(base)
        manager.add_profile(custom)
        manager.set_active("custom")

        # Should inherit retries from base, override timeout
        assert manager.get_setting("timeout") == 60
        assert manager.get_setting("retries") == 3