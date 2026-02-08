# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\chat.py\agents.py\ollama_3840b4d802f4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\chat\agents\ollama.py

import uuid

from chat.agents.open_ai import OpenAIChatAgent

from langchain_core.messages import AIMessage, HumanMessage


class OllamaChatAgent(OpenAIChatAgent):
    """

    Customization for Ollama models

    """

    async def invoke_human_input(self, state, config):

        messages = state["messages"] + [
            HumanMessage(content="Ask user what assistance they need or if they have any further query")
        ]

        response = await self.chat_model.ainvoke(messages, config={**config, "tags": ["no_stream"]})

        if isinstance(response, AIMessage) and len(response.tool_calls) == 0:
            response.tool_calls.append(
                {
                    "name": "human_input",
                    "args": {
                        "text": response.content,
                    },
                    "id": str(uuid.uuid4()),
                }
            )

        return {"messages": response}
