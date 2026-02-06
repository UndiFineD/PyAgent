# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\tests\test_agentuniverse\unit\agent_serve\test_web_booster.py
import pytest
from agentuniverse.agent_serve.web import web_booster
from agentuniverse.base.agentuniverse import AgentUniverse


def test_service():
    # os.environ['OPENAI_API_KEY'] = 'you openai api key'
    AgentUniverse().start(config_path="../agent/config.toml")
    web_booster.start_web_server(bind="127.0.0.1:8002")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
