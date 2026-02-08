# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\tests.py\integration.py\models.py\mistral.py\test_multimodal_8b12a3a29790.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\integration\models\mistral\test_multimodal.py

from agno.agent.agent import Agent

from agno.media import Image

from agno.models.mistral import MistralChat


def test_image_input():
    agent = Agent(
        model=MistralChat(id="pixtral-12b-2409"),
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run(
        "Tell me about this image.",
        images=[Image(url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")],
    )

    assert "golden" in response.content.lower()

    assert "bridge" in response.content.lower()
