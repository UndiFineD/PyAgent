# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\integration\models\together\test_multimodal.py
from agno.agent import Agent
from agno.media import Image
from agno.models.together import Together


def test_image_input():
    agent = Agent(
        model=Together(id="meta-llama/Llama-Vision-Free"),
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run(
        "Tell me about this image and give me the latest news about it.",
        images=[
            Image(
                url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
            )
        ],
    )

    assert "golden" in response.content.lower()
