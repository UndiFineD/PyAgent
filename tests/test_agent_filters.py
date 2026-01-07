import importlib.util
import sys
from pathlib import Path


def load_agent_module():
    repo_src = Path(__file__).resolve().parents[1] / 'src' / 'agent.py'
    spec = importlib.util.spec_from_file_location('agent_module', str(repo_src))
    module = importlib.util.module_from_spec(spec)
    sys.modules['agent_module'] = module
    spec.loader.exec_module(module)
    return module


def test_agents_only_filters_agent_files(tmp_path):
    # Create a small repo tree in tmp_path
    files = [
        'agent_changes.py',
        'agent_coder.py',
        'agent_context.py',
        'agent_errors.py',
        'agent_improvements.py',
        'agent_stats.py',
        'agent.py',
        'base_agent.py',
        'generate_agent_reports.py',
        'agent_backend.py',
        'agent_test_utils.py',
        'test_should_be_ignored.py',
        'random_helper.py',
    ]

    for name in files:
        p = tmp_path / name
        p.write_text('# dummy')

    agent_mod = load_agent_module()
    Agent = getattr(agent_mod, 'Agent')

    # instantiate with explicit repo_root so detection doesn't climb
    agent = Agent(repo_root=str(tmp_path), agents_only=True)
    found = agent.find_code_files()
    found_names = {p.name for p in found}

    expected = {
        'agent_changes.py',
        'agent_coder.py',
        'agent_context.py',
        'agent_errors.py',
        'agent_improvements.py',
        'agent_stats.py',
        'agent.py',
        'base_agent.py',
        'generate_agent_reports.py',
        'agent_backend.py',
        'agent_test_utils.py',
    }

    assert expected.issubset(found_names)
    # Ensure test files and unrelated helpers are excluded
    assert 'test_should_be_ignored.py' not in found_names
    assert 'random_helper.py' not in found_names
