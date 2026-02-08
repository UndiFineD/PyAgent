# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\tools.py\image_tools.py\openai_image_tools.py\toolkit_ce420e558bdb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\tools\image_tools\openai_image_tools\toolkit.py

from typing import Optional


from ...storage_handler import FileStorageHandler

from ...tool import Toolkit

from .image_analysis_openai import OpenAIImageAnalysisTool

from .image_edit import OpenAIImageEditTool

from .image_generation import OpenAIImageGenerationTool


class OpenAIImageToolkit(Toolkit):
    def __init__(
        self,
        name: str = "OpenAIImageToolkit",
        api_key: str = None,
        organization_id: str = None,
        generation_model: str = "dall-e-3",
        save_path: str = "./generated_images",
        storage_handler: Optional[FileStorageHandler] = None,
    ):
        gen_tool = OpenAIImageGenerationTool(
            api_key=api_key,
            organization_id=organization_id,
            model=generation_model,
            save_path=save_path,
            storage_handler=storage_handler,
        )

        edit_tool = OpenAIImageEditTool(
            api_key=api_key,
            organization_id=organization_id,
            save_path=save_path,
            storage_handler=storage_handler,
        )

        analysis_tool = OpenAIImageAnalysisTool(
            api_key=api_key,
            organization_id=organization_id,
            storage_handler=storage_handler,
        )

        super().__init__(name=name, tools=[gen_tool, edit_tool, analysis_tool])

        self.api_key = api_key

        self.organization_id = organization_id

        self.generation_model = generation_model

        self.save_path = save_path

        self.storage_handler = storage_handler
