# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\playground\spokenqa\download.py
from datasets import load_dataset

data = load_dataset("TwinkStart/llama-questions")
data.save_to_disk("./playground/spokenqa/llama-questions")
data = load_dataset("TwinkStart/speech-web-questions")
data.save_to_disk("./playground/spokenqa/speech-web-questions")
