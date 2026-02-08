# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\memory_layer.py\llm.py\llm_provider_a28675785171.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\memory_layer\llm\llm_provider.py

import os

from memory_layer.llm.openai_provider import OpenAIProvider

class LLMProvider:

    def __init__(self, provider_type: str, **kwargs):

        self.provider_type = provider_type

        if provider_type == "openai":

            self.provider = OpenAIProvider(**kwargs)

        else:

            raise ValueError(

                f"Unsupported provider type: {provider_type}. Supported types: 'openai'"

            )

        # TODO: add other providers

    async def generate(

        self,

        prompt: str,

        temperature: float | None = None,

        max_tokens: int | None = None,

        extra_body: dict | None = None,

        response_format: dict | None = None,

    ) -> str:

        return await self.provider.generate(

            prompt, temperature, max_tokens, extra_body, response_format

        )

