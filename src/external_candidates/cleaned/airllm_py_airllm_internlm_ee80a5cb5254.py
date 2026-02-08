# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\airllm.py\air_llm.py\airllm.py\airllm_internlm_ee80a5cb5254.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\airllm\air_llm\airllm\airllm_internlm.py

from transformers import GenerationConfig

from .airllm_base import AirLLMBaseModel

class AirLLMInternLM(AirLLMBaseModel):

    def __init__(self, *args, **kwargs):

        super(AirLLMInternLM, self).__init__(*args, **kwargs)

    def get_use_better_transformer(self):

        return False

    def get_generation_config(self):

        return GenerationConfig()

