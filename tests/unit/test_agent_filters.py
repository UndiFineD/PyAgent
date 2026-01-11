"""Unit tests for agent-specific file filtering logic."""
from importlib.machinery import ModuleSpec
import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_agent_module() -> Any:
    repo_src: Path = Path(__file__).resolve().parents[2] / 'src' / 'agent.py'
    spec: ModuleSpec | None = importlib.util.spec_from_file_location('agent_module', str(repo_src))
    module: sys.ModuleType = importlib.util.module_from_spec(spec)
    sys.modules['agent_module'] = module
    spec.loader.exec_module(module)
    return module


def test_agents_only_filters_agent_files(tmp_path: Path) -> None:
    # Create a small repo tree in tmp_path
    files: list[str] = [
        'agent_changes.py',
        'coder/code_generator.py',
        'agent_context.py',
        'errors/error_handler.py',
        'improvements/code_optimizer.py',
        'stats/metrics_collector.py',
        'agent.py',
        'base_agent/entrypoint.py',
        'generate_agent_reports.py',
        'backend/execution_engine.py',
        'test_utils/benchmarking.py',
        'test_should_be_ignored.py',
        'random_helper.py',
    ]

    for name in files:
        p: Path = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# dummy')

    agent_mod = load_agent_module()
    Agent = getattr(agent_mod, 'Agent')

    # instantiate with explicit repo_root so detection doesn't climb
    agent = Agent(repo_root=str(tmp_path), agents_only=True)
    found = agent.find_code_files()
    found_names: set[str] = {str(Path(p).relative_to(tmp_path)).replace("\\", "/") for p in found}

    expected: set[str] = {
        'agent_changes.py',
        'coder/code_generator.py',
        'agent_context.py',
        'errors/error_handler.py',
        'improvements/code_optimizer.py',
        'stats/metrics_collector.py',
        'agent.py',
        'base_agent/entrypoint.py',
        'generate_agent_reports.py',
        'backend/execution_engine.py',
        'test_utils/benchmarking.py',
    }

    assert expected.issubset(found_names)
    # Ensure test files and unrelated helpers are excluded
    assert 'test_should_be_ignored.py' not in found_names
    assert 'random_helper.py' not in found_names
