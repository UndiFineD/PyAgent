import importlib.util
import sys
from pathlib import Path
import subprocess


def load_agent_module():
    repo_src = Path(__file__).resolve().parents[1] / 'src' / 'agent.py'
    spec = importlib.util.spec_from_file_location('agent_module', str(repo_src))
    module = importlib.util.module_from_spec(spec)
    sys.modules['agent_module'] = module
    spec.loader.exec_module(module)
    return module


def test_model_env_injected(monkeypatch, tmp_path):
    agent_mod = load_agent_module()
    Agent = getattr(agent_mod, 'Agent')

    # prepare agent with models mapping
    models = {
        'coder': {'provider': 'google', 'model': 'gemini-3', 'temperature': 0.2},
        'default': {'provider': 'anthropic', 'model': 'claude-haiku', 'temperature': 0.3}
    }

    agent = Agent(repo_root=str(tmp_path), agents_only=True)
    agent.models = models

    captured = {}

    def fake_run(cmd, cwd=None, capture_output=False, text=False, timeout=None, encoding=None, errors=None, check=False, env=None):
        # record env and return success
        captured['cmd'] = cmd
        captured['env'] = env
        return subprocess.CompletedProcess(cmd, 0, stdout='ok', stderr='')

    monkeypatch.setattr(subprocess, 'run', fake_run)

    # Call _run_command simulating running agent_coder.py
    python = sys.executable
    script = str(Path('src') / 'agent_coder.py')
    res = agent._run_command([python, script, '--context'], timeout=1)

    assert res.returncode == 0
    env = captured.get('env', {})
    assert env.get('DV_AGENT_PARENT') == '1'
    assert env.get('DV_AGENT_MODEL_PROVIDER') == 'google'
    assert env.get('DV_AGENT_MODEL_NAME') == 'gemini-3'
    assert env.get('DV_AGENT_MODEL_TEMPERATURE') == '0.2'
