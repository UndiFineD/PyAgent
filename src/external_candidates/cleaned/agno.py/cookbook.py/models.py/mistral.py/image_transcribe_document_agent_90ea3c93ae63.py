# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\mistral\image_transcribe_document_agent.py
"""
This agent transcribes an old written document from an image.
"""

from agno.agent import Agent
from agno.media import Image
from agno.models.mistral.mistral import MistralChat

agent = Agent(
    model=MistralChat(id="pixtral-12b-2409"),
    markdown=True,
)

agent.print_response(
    "Transcribe this document.",
    images=[
        Image(url="https://ciir.cs.umass.edu/irdemo/hw-demo/page_example.jpg"),
    ],
)
