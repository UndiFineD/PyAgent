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

    monkeypatch.setattr(agent_mod, 'requests', type('M', (), {'post': staticmethod(fake_post)}))

    agent.register_webhook('https://example.com/webhook')

    # Run agent (dry_run; no files to process)
    agent.run()

    assert 'url' in called
    assert called['url'] == 'https://example.com/webhook'
    assert called['payload']['event'] == 'agent_complete'
