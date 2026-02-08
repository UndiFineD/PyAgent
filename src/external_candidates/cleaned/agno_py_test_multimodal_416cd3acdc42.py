# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\tests.py\integration.py\models.py\xai.py\test_multimodal_416cd3acdc42.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\integration\models\xai\test_multimodal.py

from agno.agent import Agent

from agno.media import Image

from agno.models.xai import xAI

from agno.tools.duckduckgo import DuckDuckGoTools

def test_image_input():

    agent = Agent(

        model=xAI(id="grok-2-vision-1212"),

        tools=[DuckDuckGoTools(cache_results=True)],

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

