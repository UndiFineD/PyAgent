# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\examples\sample_apps\openai_protocol_app\intelligence\agentic\agent\agent_template\openai_protocol_expressing_agent.py
from typing import Any

from agentuniverse.agent.input_object import InputObject
from agentuniverse.agent.output_object import OutputObject
from agentuniverse.agent.template.expressing_agent_template import (
    ExpressingAgentTemplate,
)
from agentuniverse.agent.template.openai_protocol_template import OpenAIProtocolTemplate
from langchain_core.runnables import RunnableSerializable


class OpenAIProtocolExpressingAgentTemplate(
    OpenAIProtocolTemplate, ExpressingAgentTemplate
):
    def parse_openai_protocol_output(self, output_object: OutputObject) -> OutputObject:
        return output_object

    def parse_input(self, input_object: InputObject, agent_input: dict) -> dict:
        self.add_output_stream(
            input_object.get_data("output_stream", None), "## Expressing  \n\n"
        )
        return super().parse_input(input_object, agent_input)
