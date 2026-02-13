# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\examples\sample_apps\openai_protocol_app\intelligence\agentic\agent\agent_template\openai_protocol_peer_agent.py
from agentuniverse.agent.template.openai_protocol_template import OpenAIProtocolTemplate
from agentuniverse.agent.template.peer_agent_template import PeerAgentTemplate


class PeerAgent(PeerAgentTemplate, OpenAIProtocolTemplate):
    pass
