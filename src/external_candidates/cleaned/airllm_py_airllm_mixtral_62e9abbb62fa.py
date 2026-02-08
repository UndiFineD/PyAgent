# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\airllm.py\air_llm.py\airllm.py\airllm_mixtral_62e9abbb62fa.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\airllm\air_llm\airllm\airllm_mixtral.py

from transformers import GenerationConfig

from .airllm_base import AirLLMBaseModel


class AirLLMMixtral(AirLLMBaseModel):
    def __init__(self, *args, **kwargs):
        super(AirLLMMixtral, self).__init__(*args, **kwargs)

    def get_use_better_transformer(self):
        return False

    def get_generation_config(self):
        return GenerationConfig()
