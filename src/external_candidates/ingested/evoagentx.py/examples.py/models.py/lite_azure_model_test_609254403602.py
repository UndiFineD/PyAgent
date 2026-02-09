# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\examples\models\lite_azure_model_test.py
import os

from dotenv import load_dotenv
from evoagentx.models import LiteLLM, LiteLLMConfig

load_dotenv()

# Create Azure OpenAI configuration
config = LiteLLMConfig(
    model="azure/" + os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # Azure model format
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
)

# Create LiteLLM client
client = LiteLLM(config=config)

# Generate response
response = client.single_generate(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        },
    ],
    max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    stream=True,
)

print(response)
