# Extracted from: C:\DEV\PyAgent\.external\llama-cpp-python\examples\high_level_api\high_level_api_embedding.py
import argparse

from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../models/7B/ggml-model.bin")
args = parser.parse_args()

llm = Llama(model_path=args.model, embedding=True)

print(llm.create_embedding("Hello world!"))
