# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\litellm\basic_hf.py
from agno.agent import Agent
from agno.models.litellm import LiteLLM

openai_agent = Agent(
    model=LiteLLM(
        id="huggingface/mistralai/Mistral-7B-Instruct-v0.2",
        top_p=0.95,
    ),
    markdown=True,
)

openai_agent.print_response("Whats happening in France?")
