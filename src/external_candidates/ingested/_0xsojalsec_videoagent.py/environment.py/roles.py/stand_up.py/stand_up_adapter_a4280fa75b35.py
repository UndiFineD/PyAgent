# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\stand_up\stand_up_adapter.py
import os

from environment.agents.base import BaseTool
from environment.config.llm import claude
from pydantic import BaseModel, Field


class StandUpAdapter(BaseTool):
    """
    Application scenario: Stand-up comedy Creating
    Adapt a reference script into segmented stand-up comedy.
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(
            ..., description="User requirements for creating stand-up comedy script"
        )
        ref_script_path: str = Field(
            ..., description="File path to the reference script"
        )

    class OutputSchema(BaseModel):
        script: str = Field(
            ..., description="String of segmented stand-up comedy script"
        )

    def execute(self, **kwargs):

        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        reqs = params.reqs
        ref_script_path = params.ref_script_path
        data_dir = os.path.dirname(ref_script_path)

        with open(ref_script_path, "r", encoding="utf-8") as f:
            ref_script = f.read().strip()

        print("Creating Stand-up comedy script...")

        user_prompt = f"""
        You are a professional stand-up comedy adaptation specialist. 
        Adapt the following reference script into a stand-up comedy format.

        Content to adapt: 
        {ref_script}

        Additional requirements:
        {reqs}

        Format specifications:
        1. Each line must begin with one of these tone markers: [Natural] [Confused] [Empathetic] [Exclamatory]
        2. Add atmosphere cues [Laughter] or [Cheers] at key moments (immediately after dialogue)
        3. Keep each line independent using this structure:
            [Tone marker]...
            [Tone marker]...[Atmosphere cue (if applicable)]

        Important notes:
        - Do NOT include titles, introductions or conclusions
        - Preserve the core humor while localizing cultural references
        - Incorporate linguistic features and rhythm of English stand-up
        - Use atmosphere cues sparingly and only at pivotal moments

        Generate a 3-5 minute performance script following these requirements, ensuring every line has tone markers and key punchlines include atmosphere cues.
        Atmosphere cues (quantity: 3-4)
        Directly output the title and script without any other explanations
        Example output:
        # title
        [Tone marker]...
        [Tone marker]...
        ...
        """

        try:
            response = claude(user=user_prompt)
            script = response.choices[0].message.content

            output_path = os.path.join(os.path.dirname(ref_script_path), "stand-up.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(script)

            return {"script": script}
        except Exception as e:
            print(f"Error in talk show writing: {str(e)}")
            return
