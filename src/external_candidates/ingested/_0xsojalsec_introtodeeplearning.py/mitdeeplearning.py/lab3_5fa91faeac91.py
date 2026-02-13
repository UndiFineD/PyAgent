# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-introtodeeplearning\mitdeeplearning\lab3.py
import os

from datasets import load_dataset
from openai import OpenAI
from torch.utils.data import DataLoader

cwd = os.path.dirname(__file__)


def create_dataloader(style):
    ds = load_dataset("databricks/databricks-dolly-15k", split="train")
    with open(os.path.join(cwd, f"data/text_styles/{style}.txt"), "r") as f:
        new_responses = [line.strip().replace("\\n", "\n") for line in f]

    # Update the entire dataset at once with the new responses
    ds_ = ds.select(range(len(new_responses)))
    ds_ = ds_.map(
        lambda x, idx: {"response_style": new_responses[idx]},
        with_indices=True,
        num_proc=1,
    )

    n = len(new_responses)
    ds_test = ds.select(range(n, n + n))

    # Create a dataloader
    dataloader = DataLoader(ds_, batch_size=1, shuffle=True)
    dataloader_test = DataLoader(ds_test, batch_size=1, shuffle=True)
    return dataloader, dataloader_test


class LLMClient:
    def __init__(
        self, model: str, api_key: str, api_base: str = "https://openrouter.ai/api/v1"
    ):
        self.llm_client = OpenAI(api_key=api_key, base_url=api_base)
        self.model = model

    def ask(self, user: str, system: str = None, **kwargs):
        messages = [{"role": "user", "content": user}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
        res = self.llm_client.chat.completions.create(
            model=self.model, messages=messages, **kwargs
        )
        return res


yoda_test_text = (
    "Wisdom, sought by many, found by few, it is. Haste not, patience have. "
    "For in stillness, answers come. Much to learn, still you have. "
    "Fear leads to anger; anger, to hate. Down the dark path, guide you it will. "
    "Trust the Force, you must. Powerful ally it is. Life it creates, surrounds, binds. "
    "Adventure, excitement, a Jedi craves not these things. Discipline, balance, seek you should. "
    "Hmm, clearer now is the path, yes? Help you more, I can, if needed it is. "
    "Endless, the journey of learning is. Stay true to your path, and clarity you will find. "
    "Remember, the Force flows through all, but your heart determines how it shapes your destiny. "
    "Much more to teach, I have. Ready, are you? Mmm."
)


# class Llama(LLMClient):
#     def __init__(self, api_key: str):
#         """
#         Initialize the LlamaFree model client.

#         LlamaFree is available from LlamaFree.
#         Provide your LlamaFree API key (`api_key`) to access.
#         """
#         # super().__init__(model="meta-llama/llama-3.2-3b-instruct", api_key=api_key)
#         super().__init__(model="meta-llama/llama-3.1-8b-instruct", api_key=api_key)


# class LFM40B(LLMClient):
#     def __init__(self, api_key: str):
#         """
#         Initialize the LFM-40B model client.

#         LFM-40B is available from Lambda Labs.
#         Provide your Lambda Labs API key (`api_key`) to access.
#         """
#         api_base = "https://api.lambdalabs.com/v1"
#         super().__init__(model="lfm-40b", api_base=api_base, api_key=api_key)
