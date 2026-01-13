"""Unit tests for model propagation logic across agents."""
import importlib.util
import sys
from pathlib import Path
import subprocess
from typing import Any


def load_agent_module() -> Any:
    repo_root: Path = Path(__file__).resolve().parents[2]
    src_dir: Path = repo_root / 'src'
    if str(repo_root) not in sys.path:

    import src.core.base.BaseAgent.agent as agent_module
    return agent_module


def test_model_env_injected(monkeypatch, tmp_path) -> None:
    agent_mod: Any = load_agent_module()
    Agent = getattr(agent_mod, 'BaseAgent')

    # prepare agent with models mapping
    models = {
        'coder': {'provider': 'google', 'model': 'gemini-3', 'temperature': 0.2},
        'default': {'provider': 'anthropic', 'model': 'claude-haiku', 'temperature': 0.3}
    }

    agent = Agent(file_path=str(tmp_path / 'agent.py'))
    agent.models = models

    captured = {}

    def fake_run(cmd, cwd=None, capture_output=False, text=False, timeout=None, encoding=None, errors=None, check=False, env=None) -> subprocess.CompletedProcess[str]:
        # record env and return success
        captured['cmd'] = cmd
        captured['env'] = env
        return subprocess.CompletedProcess(cmd, 0, stdout='ok', stderr='')

    monkeypatch.setattr(subprocess, 'run', fake_run)

    # Call _run_command simulating running agent_coder.py
    python: str = sys.executable
    script = str(Path('src') / 'agent_coder.py')
    res = agent._run_command([python, script, '--context'], timeout=1)

    assert res.returncode == 0
    env = captured.get('env', {})
    assert env.get('DV_AGENT_PARENT') == '1'
    assert env.get('DV_AGENT_MODEL_PROVIDER') == 'google'
    assert env.get('DV_AGENT_MODEL_NAME') == 'gemini-3'
    assert env.get('DV_AGENT_MODEL_TEMPERATURE') == '0.2'
