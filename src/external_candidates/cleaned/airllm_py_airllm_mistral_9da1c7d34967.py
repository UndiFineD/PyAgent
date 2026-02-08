# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\airllm.py\air_llm.py\airllm.py\airllm_mistral_9da1c7d34967.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\airllm\air_llm\airllm\airllm_mistral.py

from transformers import GenerationConfig

from .airllm_base import AirLLMBaseModel

class AirLLMMistral(AirLLMBaseModel):

    def __init__(self, *args, **kwargs):

        super(AirLLMMistral, self).__init__(*args, **kwargs)

    def get_use_better_transformer(self):

        return False

    def get_generation_config(self):

        return GenerationConfig()

