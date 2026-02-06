# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\cross_talk\cross_talk_adapter.py
import os

from environment.agents.base import BaseTool
from environment.config.llm import claude
from pydantic import BaseModel, Field


class CrossTalkAdapter(BaseTool):
    """
    Application scenario: Cross Talk Creating
    Adapt a reference script into segmented cross talk.
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(
            ..., description="User requirements for creating cross talk script"
        )
        ref_script_path: str = Field(
            ..., description="File path to the reference script"
        )
        dou_gen_dir: str = Field(
            ..., description="The 逗哏 tone directory for cross talk synthesis."
        )
        peng_gen_dir: str = Field(
            ..., description="The 捧哏 tone directory for cross talk synthesis."
        )

    class OutputSchema(BaseModel):
        script: str = Field(..., description="String of segmented cross talk script")

    def execute(self, **kwargs):

        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        reqs = params.reqs
        ref_script_path = params.ref_script_path
        dou_gen_dir = params.dou_gen_dir
        peng_gen_dir = params.peng_gen_dir
        data_dir = os.path.dirname(ref_script_path)

        dou_gen_name = os.path.basename(dou_gen_dir)
        peng_gen_name = os.path.basename(peng_gen_dir)

        with open(ref_script_path, "r", encoding="utf-8") as f:
            ref_script = f.read().strip()

        user_prompt = f"""
        You are a professional cross talk (xiang sheng) adaptation specialist. Please adapt the following English stand-up comedy material into an authentic traditional Chinese crosstalk dialogue format.

        Material to adapt:  
        {ref_script}

        Crosstalk roles:
        - {dou_gen_name}: Comic lead (逗哏), delivers main jokes and drives the narrative
        - {peng_gen_name}: Straight man (捧哏), reacts and plays off the comic lead

        Format Requirements:
        1. Each performer's lines must be on separate lines starting with their name.
        2. Begin each line with one tone marker: [Natural] or [Confused] or [Emphatic]. 
           The same tone should not appear consecutively for more than two lines.
        
        Example:
        [tone] Role name: ... 
        [tone] Role name: ...

        Additional requirements:
        {reqs}

        Guidelines:
        - The first line of the output should be the title of the crosstalk.
        - Preserve core humor while localizing cultural references
        - Incorporate traditional crosstalk speech patterns and rhythm
        - Use common crosstalk phrases and interactive elements

        Output ONLY the adapted title and dialogue without any formatting symbols or explanations.
        """

        try:
            response = claude(user=user_prompt)
            script = response.choices[0].message.content

            output_path = os.path.join(
                os.path.dirname(ref_script_path), "cross-talk.txt"
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(script)

            return {"script": script}
        except Exception as e:
            print(f"Error in talk show writing: {str(e)}")
            return
