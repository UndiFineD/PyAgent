# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\airllm.py\air_llm.py\airllm.py\airllm_baichuan_ed0f2549f477.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\airllm\air_llm\airllm\airllm_baichuan.py

from transformers import GenerationConfig

from .airllm_base import AirLLMBaseModel

from .tokenization_baichuan import BaichuanTokenizer


class AirLLMBaichuan(AirLLMBaseModel):
    def __init__(self, *args, **kwargs):
        super(AirLLMBaichuan, self).__init__(*args, **kwargs)

    def get_use_better_transformer(self):
        return False

    def get_tokenizer(self, hf_token=None):
        # use this hack util the bug is fixed: https://huggingface.co/baichuan-inc/Baichuan2-7B-Base/discussions/2

        return BaichuanTokenizer.from_pretrained(self.model_local_path, use_fast=False, trust_remote_code=True)

    def get_generation_config(self):
        return GenerationConfig()
