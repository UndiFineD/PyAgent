# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\run_qwq_demo.py

from dotenv import load_dotenv

load_dotenv()

import os
from typing import Dict, List

from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.toolkits import *
from camel.types import ModelPlatformType, ModelType
from loguru import logger
from retry import retry
from utils import OwlRolePlaying, run_society


def construct_society(question: str) -> OwlRolePlaying:
    r"""Construct the society based on the question."""

    user_role_name = "user"
    assistant_role_name = "assistant"

    user_model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="qwq-32b",
        api_key=os.getenv("QWEN_API_KEY"),
        url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_config_dict={"temperature": 0.4, "max_tokens": 4096},
    )

    assistant_model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="qwq-32b",
        api_key=os.getenv("QWEN_API_KEY"),
        url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_config_dict={"temperature": 0.4, "max_tokens": 4096},
    )

    tools_list = [
        *WebToolkit(
            headless=False,  # Set to True if you want to run in headless mode (e.g. on a remote server)
            web_agent_model=assistant_model,
            planning_agent_model=assistant_model,
        ).get_tools(),
        *DocumentProcessingToolkit().get_tools(),
        # *VideoAnalysisToolkit(model=assistant_model).get_tools(),  # This requires OpenAI Key
        # *AudioAnalysisToolkit().get_tools(),  # This requires OpenAI Key
        *CodeExecutionToolkit().get_tools(),
        *ImageAnalysisToolkit(model=assistant_model).get_tools(),
        *SearchToolkit(model=assistant_model).get_tools(),
        *ExcelToolkit().get_tools(),
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
