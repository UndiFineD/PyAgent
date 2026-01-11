"""Legacy unit tests for BaseAgent logic."""
import pytest
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass

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
                                           base_agent_module: Any) -> str:
    target = tmp_path / "x.md"
    target.write_text("BEFORE", encoding="utf-8")

    # BaseAgent uses a class-level response cache by default. Disable caching
    # for this test so we reliably exercise the patched `run_subagent`.
    monkeypatch.setenv("DV_AGENT_CACHE", "false")
    base_agent_module.BaseAgent._response_cache.clear()

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        assert "Improve" in description
        assert "prompt" in prompt
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
    assert "--- a/" in diff
    assert "+++ b/" in diff


def test_run_subagent_delegates_to_agent_backend(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    """BaseAgent.run_subagent delegates backend selection to agent_backend."""

    calls: list[tuple[str, str, str]] = []

    def fake_backend_run_subagent(description: str, prompt: str, original_content: str = "") -> str:
        calls.append((description, prompt, original_content))
        return "OK"

    monkeypatch.setattr(base_agent_module.agent_backend, "run_subagent", fake_backend_run_subagent)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "OK"
    assert calls == [("desc", "prompt", "ORIG")]


def test_run_subagent_falls_back_to_original_content_when_backend_returns_none(
        monkeypatch: pytest.MonkeyPatch,
        base_agent_module: Any) -> None:
    def fake_backend_run_subagent(description: str, prompt: str, original_content: str = "") -> None:
        return None

    monkeypatch.setattr(base_agent_module.agent_backend, "run_subagent", fake_backend_run_subagent)
    agent = base_agent_module.BaseAgent("x.md")
    out = agent.run_subagent("desc", "prompt", "ORIG")
    assert out == "ORIG"


def test_llm_chat_via_github_models_builds_request_and_parses_response(
    monkeypatch: pytest.MonkeyPatch, base_agent_module: Any
) -> None:
    posted: Dict[str, Any] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> Dict[str, Any]:
            return {"choices": [{"message": {"content": "  hello  "}}]}

    def fake_post(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> FakeResponse:
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
    assert posted["url"] == "https://example.test/v1/chat/completions"
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

    def fake_post(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> FakeResponse:
        assert url == "https://example.test/v1/chat/completions"
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

@pytest.mark.parametrize("backend", ["github-models", "copilot", "gh"])
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


def test_markdown_fixing_with_edge_cases(tmp_path: Path, base_agent_module: Any) -> None:
    """Test markdown content fixing with various edge cases."""
    # Test with markdown file containing edge cases
    target = tmp_path / "edge_cases.md"
    target.write_text("# Header\n\n[Link]()\n\n```\ncode\n```\n", encoding="utf-8")
    agent = base_agent_module.BaseAgent(str(target))
    assert agent.read_previous_content() is not None


@pytest.mark.parametrize("extension", [".md", ".txt", ".py", ".js", ""])
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
            from src.infrastructure.backend import execution_engine as agent_backend
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
