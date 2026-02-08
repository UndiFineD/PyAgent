# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\tests.py\integration.py\models.py\aws.py\bedrock.py\test_multimodal_2671b7dc255f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\integration\models\aws\bedrock\test_multimodal.py

from pathlib import Path

from agno.agent.agent import Agent

from agno.media import Image

from agno.models.aws import AwsBedrock

def test_image_input_bytes():

    """

    Only bytes input is supported for multimodal models

    """

    agent = Agent(

        model=AwsBedrock(id="amazon.nova-pro-v1:0"),

        markdown=True,

        telemetry=False,

        monitoring=False,

    )

    image_path = Path(__file__).parent.parent.parent.joinpath("sample_image.jpg")

    # Read the image file content as bytes

    image_bytes = image_path.read_bytes()

    response = agent.run(

        "Tell me about this image.",

        images=[Image(content=image_bytes, format="jpeg")],

    )

    assert "bridge" in response.content.lower()

