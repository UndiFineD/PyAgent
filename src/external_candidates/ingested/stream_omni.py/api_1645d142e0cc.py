# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\api.py
# Usage:
# # controller
# python stream_omni/serve/controller.py --host 0.0.0.0 --port 10000 &

# # CosyVoice worker
# COSYVOICE_CKPT=path_to_CosyVoice-300M-25Hz
# WAV_DIR=path_to_save_generated_audio
# CUDA_VISIBLE_DEVICES=0 PYTHONPATH=CosyVoice/third_party/Matcha-TTS python /CosyVoice/cosyvoice_worker.py --port 21003 --model ${COSYVOICE_CKPT} --wav_dir ./gen_wavs/

# # Stream-Omni worker, add --load-8bit for VRAM lower than 32GB
# STREAMOMNI_CKPT=path_to_stream-omni-8b
# CUDA_VISIBLE_DEVICES=1  python stream_omni/serve/model_worker.py --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path ${STREAMOMNI_CKPT} --model-name stream-omni &

# python api.py


import base64
import json
import os
import time

import requests
from PIL import Image

### Image
image_path = "./stream_omni/serve/examples/cat.jpg"
with open(image_path, "rb") as img_file:
    image_bytes = img_file.read()
image_base64 = base64.b64encode(image_bytes).decode("utf-8")


### Speech
def speech_to_token_from_file(file_path):
    url = "http://localhost:21003/speech_to_token"  # The FastAPI endpoint
    headers = {
        "accept": "application/json",
    }
    # Open the file in binary mode and send it as part of the request
    with open(file_path, "rb") as file:
        files = {
            "file": (file.name, file, "audio/wav")
        }  # Name, file object, and file type
        response = requests.post(url, headers=headers, files=files)

    # Handle the response (assumed to be JSON based on the FastAPI code)
    if response.status_code == 200:
        return response.json()  # Returns the response in JSON format (contains tokens)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def token_to_speech_from_tokens(tokens):
    url = "http://localhost:21003/token_to_speech"  # The FastAPI endpoint
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    # Create the payload with the tokens
    data = {"tokens": tokens}

    # Send the POST request with the JSON data
    response = requests.post(url, headers=headers, json=data)

    # Handle the response
    if response.status_code == 200:
        # Assuming the response contains the path to the generated audio file
        return response.json()  # Contains the audio file path or URL
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


audio_path = "./stream_omni/serve/examples/cat_color.wav"
speech_token = speech_to_token_from_file(audio_path)["tokens"]

### LLM
pload = {
    "model": "stream-omni",
    "prompt": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful language and vision assistant. You are able to understand the visual content that the user provides, and assist the user with a variety of tasks using natural language.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n<image>\n{speech_token}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    "temperature": 0.0,
    "top_p": 1.0,
    "max_new_tokens": 1024,
    "inference_type": "speech_to_speech",
    "stop": "<|eot_id|>",
    "images": [image_base64],
}
response = requests.post(
    "http://localhost:40000/worker_generate_stream",
    headers={"User-Agent": "LLaVA Client"},
    json=pload,
    stream=True,
    timeout=100,
)


for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
    if chunk:
        data = json.loads(chunk.decode())
        print(data)
