# Extracted from: C:\DEV\PyAgent\.external\abetlen-llama-cpp-python\examples\high_level_api\high_level_api_streaming.py
import argparse
import json

from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../models/7B/ggml-models.bin")
args = parser.parse_args()

llm = Llama(model_path=args.model)

stream = llm(
    "Question: What are the names of the planets in the solar system? Answer: ",
    max_tokens=48,
    stop=["Q:", "\n"],
    stream=True,
)

for output in stream:
    print(json.dumps(output, indent=2))
