# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\abetlen_llama_cpp_python.py\examples.py\ray.py\llm_2a69464c886c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\abetlen-llama-cpp-python\examples\ray\llm.py

from typing import Dict

from llama_cpp import Llama

from ray import serve

from ray.serve import Application

from starlette.requests import Request


@serve.deployment
class LlamaDeployment:
    def __init__(self, model_path: str):
        self._llm = Llama(model_path=model_path)

    async def __call__(self, http_request: Request) -> Dict:
        input_json = await http_request.json()

        prompt = input_json["prompt"]

        max_tokens = input_json.get("max_tokens", 64)

        return self._llm(prompt, max_tokens=max_tokens)


def llm_builder(args: Dict[str, str]) -> Application:
    return LlamaDeployment.bind(args["model_path"])
