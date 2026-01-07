import importlib.util
import sys
from pathlib import Path


def load_agent_module():
    repo_src = Path(__file__).resolve().parents[1] / 'src'
    if str(repo_src) not in sys.path:
        sys.path.insert(0, str(repo_src))
    agent_path = repo_src / 'agent.py'
    spec = importlib.util.spec_from_file_location('agent_module', str(agent_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules['agent_module'] = module
    spec.loader.exec_module(module)
    return module


def test_webhooks_sent_on_run(monkeypatch, tmp_path):
    agent_mod = load_agent_module()
    Agent = getattr(agent_mod, 'Agent')

    # Create a minimal repo root
    (tmp_path / 'README.md').write_text('# repo')

    agent = Agent(repo_root=str(tmp_path), dry_run=True, max_files=0)
    # register a webhook
    called = {}

    def fake_post(url, json, timeout):
        called['url'] = url
        called['payload'] = json
        class R: pass
        r = R()
        r.status_code = 200
        return r

    # Ensure requests is available in the module namespace
    try:
        import requests as _requests
    except Exception:
        _requests = None

    # Patch the Agent module where it's used
    import sys
    # Find the module in sys.modules
    agent_mod_internal = sys.modules.get('src.classes.agent.Agent') or sys.modules.get('classes.agent.Agent')
    if agent_mod_internal:
        monkeypatch.setattr(agent_mod_internal, 'requests', type('M', (), {'post': staticmethod(fake_post)}))
        monkeypatch.setattr(agent_mod_internal, 'HAS_REQUESTS', True)
    else:
        # Fallback to string based if not loaded (unlikely)
        try:
            monkeypatch.setattr('src.classes.agent.Agent.requests', type('M', (), {'post': staticmethod(fake_post)}), raising=False)
            monkeypatch.setattr('src.classes.agent.Agent.HAS_REQUESTS', True, raising=False)
        except Exception:
            monkeypatch.setattr('classes.agent.Agent.requests', type('M', (), {'post': staticmethod(fake_post)}), raising=False)
            monkeypatch.setattr('classes.agent.Agent.HAS_REQUESTS', True, raising=False)

    agent.register_webhook('https://example.com/webhook')

    # Run agent (dry_run; no files to process)
    agent.run()

    assert 'url' in called
    assert called['url'] == 'https://example.com/webhook'
    assert called['payload']['event'] == 'agent_complete'
