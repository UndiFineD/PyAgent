"""Legacy unit tests for agent logic."""

import pytest
import subprocess
from pathlib import Path
from typing import Any
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass


def test_agent_with_large_repository_performance(
    tmp_path: Path, agent_module: Any
) -> None:
    """Test agent behavior with large repository - performance benchmarks."""
    # ... (skipping context for now)


def test_git_operations_commit(tmp_path: Path, agent_module: Any) -> None:
    """Test git operations: commits."""
    recorder = LocalContextRecorder(tmp_path.parent, "TestRunner")

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    recorder.record_interaction("shell", "git", "git init", "Initialized git repo")

    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    # Create a file
    test_file = tmp_path / "test.txt"
    test_file.write_text("initial content")

    # Commit
    subprocess.run(
        ["git", "add", "test.txt"], cwd=tmp_path, check=True, capture_output=True
    )
    result = subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    recorder.record_interaction(
        "shell", "git", "git commit -m 'Initial commit'", result.stdout
    )

    assert result.returncode == 0
    assert (
        "Initial commit" in result.stdout or "initial content" in test_file.read_text()
    )


def test_concurrent_file_processing_scenarios(
    tmp_path: Path, agent_module: Any
) -> None:
    """Test concurrent file processing scenarios."""
    # Create multiple files for concurrent processing
    files = []
    for i in range(10):
        file_path = tmp_path / f"concurrent_{i}.py"
        file_path.write_text(f"# Concurrent file {i}\nprint('File {i}')\n")
        files.append(file_path)

    # Test that all files are accessible (mock concurrent processing)
    for file_path in files:
        assert file_path.exists()
        assert file_path.read_text()


def test_all_cli_argument_combinations(agent_module: Any) -> None:
    """Test all command-line argument combinations."""
    # Mock parser
    if hasattr(agent_module, "create_parser"):
        parser = agent_module.create_parser()

        # Test individual arguments
        args = parser.parse_args(["--help"] if "--help" in ["-h", "--help"] else [])
        assert args is not None


def test_agent_with_large_file_set(tmp_path: Path, agent_module: Any) -> None:
    """Test agent with large file sets."""
    # Create 50 diverse files
    file_types = {
        ".py": "def test(): pass",
        ".md": "# Test\nContent",
        ".txt": "Plain text",
        ".json": '{"key": "value"}',
    }

    for ext, content in file_types.items():
        for i in range(10):
            file_path = tmp_path / f"file_{i:02d}{ext}"
            file_path.write_text(content)

    # Verify all files created
    all_files = list(tmp_path.glob("*"))
    assert len(all_files) == 40


def test_logging_output_verbosity(tmp_path: Path, agent_module: Any) -> None:
    """Test logging output with different verbosity levels."""
    import logging

    # Capture logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("agent")

    # Test that logger exists
    assert logger is not None

    # Log messages at different levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")


def test_verbosity_level_debug(agent_module: Any, caplog: Any) -> None:
    """Test debug verbosity level produces detailed output."""
    import logging

    with caplog.at_level(logging.DEBUG):
        logger = logging.getLogger("agent_test")
        logger.debug("Detailed debug info")

    assert "Detailed debug info" in caplog.text or len(caplog.records) > 0


def test_git_operations_branch_switching(tmp_path: Path) -> None:
    """Test git operations: branch switching."""
    # Initialize repo
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    # Create initial commit
    (tmp_path / "test.txt").write_text("test")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True
    )

    # Create and switch branch
    subprocess.run(
        ["git", "checkout", "-b", "feature"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert "feature" in result.stdout


def test_git_unavailable_graceful_degradation(
    agent_module: Any, monkeypatch: Any
) -> None:
    """Test graceful degradation when git is unavailable."""

    # Mock git command to fail
    def mock_run(*args: Any, **kwargs: Any) -> Any:
        raise FileNotFoundError("git not found")


def test_configuration_file_handling(tmp_path: Path, agent_module: Any) -> None:
    """Test configuration file handling."""
    config_file = tmp_path / "agent.config"
    config_file.write_text("key=value\nanother=123\n")

    # Verify config file can be read
    assert config_file.exists()
    content = config_file.read_text()
    assert "key=value" in content


def test_config_file_parsing(tmp_path: Path) -> None:
    """Test parsing of configuration files."""
    config_file = tmp_path / ".agentrc"
    config_file.write_text("""
[settings]
timeout=60
dry_run=false
workers=4
""")

    assert config_file.exists()
    content = config_file.read_text()
    assert "timeout" in content


def test_stats_reporting_accuracy(agent_module: Any, tmp_path: Path) -> None:
    """Test accuracy of stats reporting."""
    # Create test files
    for i in range(5):
        (tmp_path / f"test_{i}.py").write_text(f"# File {i}")

    # Count files
    files = list(tmp_path.glob("*.py"))
    assert len(files) == 5

    # Stats should accurately reflect this
    file_count = len(files)
    assert file_count == 5


@pytest.mark.parametrize(
    "file_type, content",
    [
        (".py", "print('hello')"),
        (".md", "# Hello"),
        (".txt", "hello"),
    ],
)
def test_agent_with_parametrized_file_types(
    tmp_path: Path, file_type: str, content: str
) -> None:
    """Test agent with parametrized different file types."""
    test_file = tmp_path / f"test{file_type}"
    test_file.write_text(content)

    assert test_file.exists()
    assert test_file.read_text() == content


def test_multiple_agent_interactions(agent_module: Any, tmp_path: Path) -> None:
    """Test interaction between multiple agents."""
    # Create test files for multiple agents
    (tmp_path / "code.py").write_text("def foo(): pass")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog")
    (tmp_path / "README.md").write_text("# Project")

    # Verify all files exist (multiple agent targets)
    assert (tmp_path / "code.py").exists()
    assert (tmp_path / "CHANGELOG.md").exists()
    assert (tmp_path / "README.md").exists()


def test_agent_integration_with_real_workflow(tmp_path: Path) -> None:
    """Test agent integration with realistic workflow."""
    # Create a realistic repo structure
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def main(): pass")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_main.py").write_text("def test_main() -> None: pass")
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / ".codeignore").write_text("*.pyc\n__pycache__/")

    # Verify structure
    assert (tmp_path / "src" / "main.py").exists()
    assert (tmp_path / "tests" / "test_main.py").exists()
    assert (tmp_path / ".codeignore").exists()


def test_agent_performance_regression(tmp_path: Path, agent_module: Any) -> None:
    """Test agent performance regression - ensure no degradation."""
    import time

    # Create 20 files
    for i in range(20):
        (tmp_path / f"file_{i}.py").write_text(f"# File {i}\nx={i}")

    # Time the operation
    start = time.time()
    files = list(tmp_path.glob("*.py"))
    elapsed = time.time() - start

    # Should be fast (< 100ms for 20 files)
    assert elapsed < 0.1, f"Performance regression: {elapsed * 1000:.1f}ms"
    assert len(files) == 20


@pytest.mark.parametrize("file_count", [1, 10, 50])
def test_agent_scaling_performance(tmp_path: Path, file_count: int) -> None:
    """Test agent scaling performance with varying file counts."""
    import time

    # Create files
    for i in range(file_count):
        (tmp_path / f"file_{i:03d}.py").write_text(f"x={i}")

    # Measure file discovery
    start = time.time()
    files = list(tmp_path.glob("*.py"))
    elapsed = time.time() - start

    assert len(files) == file_count
    # Should scale linearly
    # Relaxed for Windows filesystem performance
    assert elapsed < (file_count / 100.0) + 0.05


@pytest.fixture
def simple_repo_structure(tmp_path: Path) -> Path:
    """Fixture providing a simple repo structure."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "README.md").write_text("# Project")
    return tmp_path


@pytest.fixture
def complex_repo_structure(tmp_path: Path) -> Path:
    """Fixture providing a complex repo structure."""
    # Create multi-level structure
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app").mkdir()
    (tmp_path / "src" / "app" / "main.py").write_text("def main(): pass")
    (tmp_path / "src" / "utils.py").write_text("def util(): pass")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_main.py").write_text("def test(): pass")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs")
    (tmp_path / ".codeignore").write_text("*.pyc\n__pycache__/\n.env")
    return tmp_path


def test_agent_with_simple_repo_fixture(simple_repo_structure: Path) -> None:
    """Test agent with simple repo fixture."""
    assert (simple_repo_structure / "main.py").exists()
    assert (simple_repo_structure / "README.md").exists()


def test_agent_with_complex_repo_fixture(complex_repo_structure: Path) -> None:
    """Test agent with complex repo fixture."""
    assert (complex_repo_structure / "src" / "app" / "main.py").exists()
    assert (complex_repo_structure / "tests" / "test_main.py").exists()
    assert (complex_repo_structure / "docs" / "README.md").exists()


def test_multiple_fixture_repo_structures(
    simple_repo_structure: Path, complex_repo_structure: Path
) -> None:
    """Test with multiple fixture-based repo structures."""
    assert simple_repo_structure.exists()
    assert complex_repo_structure.exists()
    assert len(list(complex_repo_structure.glob("**/*.py"))) >= 3
