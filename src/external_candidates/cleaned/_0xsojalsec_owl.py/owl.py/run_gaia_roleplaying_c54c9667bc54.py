# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\run_gaia_roleplaying.py
import os
import shutil

from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.toolkits import *
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv
from loguru import logger
from retry import retry
from utils import GAIABenchmark

load_dotenv()


LEVEL = 1
SAVE_RESULT = True
test_idx = [0]


def main():
    cache_dir = "tmp/"
    os.makedirs(cache_dir, exist_ok=True)

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
            headless=False,  # Set to True if you want to run in headless mode (e.g. on a remote server)
            web_agent_model=assistant_model,
            planning_agent_model=assistant_model,
        ).get_tools(),
        *DocumentProcessingToolkit().get_tools(),
        *VideoAnalysisToolkit(model=assistant_model).get_tools(),  # This requires OpenAI Key
        *AudioAnalysisToolkit().get_tools(),  # This requires OpenAI Key
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        *ImageAnalysisToolkit(model=assistant_model).get_tools(),
        *SearchToolkit(model=assistant_model).get_tools(),
        *ExcelToolkit().get_tools(),
    ]

    user_role_name = "user"
    user_agent_kwargs = dict(model=user_model)
    assistant_role_name = "assistant"
    assistant_agent_kwargs = dict(model=assistant_model, tools=tools_list)

    benchmark = GAIABenchmark(data_dir="data/gaia", save_to=f"results/result.json")

    print(f"Number of validation examples: {len(benchmark.valid)}")
    print(f"Number of test examples: {len(benchmark.test)}")

    result = benchmark.run(
        on="valid",
        level=LEVEL,
        idx=test_idx,
        save_result=SAVE_RESULT,
        user_role_name=user_role_name,
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name=assistant_role_name,
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    logger.success(f"Correct: {result['correct']}, Total: {result['total']}")
    logger.success(f"Accuracy: {result['accuracy']}")


if __name__ == "__main__":
    main()
