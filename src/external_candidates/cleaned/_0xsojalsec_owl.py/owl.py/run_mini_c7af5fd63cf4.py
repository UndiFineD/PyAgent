# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\run_mini.py
from dotenv import load_dotenv

load_dotenv()

import os
from typing import Dict, List

from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.toolkits import (
    AudioAnalysisToolkit,
    CodeExecutionToolkit,
    DocumentProcessingToolkit,
    ExcelToolkit,
    FunctionTool,
    ImageAnalysisToolkit,
    SearchToolkit,
    VideoAnalysisToolkit,
    WebToolkit,
)
from camel.types import ModelPlatformType, ModelType
from loguru import logger
from retry import retry
from utils import OwlRolePlaying, run_society


def construct_society(question: str) -> OwlRolePlaying:
    r"""Construct the society based on the question."""

    user_role_name = "user"
    assistant_role_name = "assistant"

    user_model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig(temperature=0, top_p=1).as_dict(),  # [Optional] the config for model
    )

    assistant_model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig(temperature=0, top_p=1).as_dict(),  # [Optional] the config for model
    )

    tools_list = [
        *WebToolkit(
            headless=False,
            web_agent_model=assistant_model,
            planning_agent_model=assistant_model,
        ).get_tools(),
        # *DocumentProcessingToolkit().get_tools(),
        # *VideoAnalysisToolkit(model=assistant_model).get_tools(),  # This requires OpenAI Key
        # *AudioAnalysisToolkit().get_tools(),  # This requires OpenAI Key
        # *CodeExecutionToolkit().get_tools(),
        # *ImageAnalysisToolkit(model=assistant_model).get_tools(),
        FunctionTool(SearchToolkit(model=assistant_model).search_duckduckgo),
        # *ExcelToolkit().get_tools()
    ]

    user_role_name = "user"
    user_agent_kwargs = dict(model=user_model)
    assistant_role_name = "assistant"
    assistant_agent_kwargs = dict(model=assistant_model, tools=tools_list)

    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    society = OwlRolePlaying(
        **task_kwargs,
        user_role_name=user_role_name,
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name=assistant_role_name,
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society


# Example case
question = "What was the volume in m^3 of the fish bag that was calculated in the University of Leicester paper `Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?` "

society = construct_society(question)
answer, chat_history, token_count = run_society(society)

logger.success(f"Answer: {answer}")
