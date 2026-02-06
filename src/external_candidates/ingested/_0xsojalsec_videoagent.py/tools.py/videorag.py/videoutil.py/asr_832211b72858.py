# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\_videoutil\asr.py
import logging
import os

import torch
from tqdm import tqdm
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def speech_to_text(video_name, working_dir, segment_index2name, audio_output_format):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    tools_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

    # Path to the local whisper model
    model_path = os.path.join(tools_dir, "whisper-large-v3-turbo")

    # Check if the model directory exists
    if not os.path.exists(model_path):
        logging.warning(
            f"Local model not found at {model_path}, falling back to loading from Hugging Face"
        )
        model_id = "whisper-large-v3-turbo"
    else:
        model_id = model_path
        logging.info(f"Using local whisper model from: {model_path}")

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        use_safetensors=True,
        local_files_only=(
            model_id == model_path
        ),  # Only use local files if using local path
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(
        model_id, local_files_only=(model_id == model_path)
    )

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    cache_path = os.path.join(working_dir, "_cache", video_name)

    transcripts = {}
    for index in tqdm(segment_index2name, desc=f"Speech Recognition {video_name}"):
        segment_name = segment_index2name[index]
        audio_file = os.path.join(cache_path, f"{segment_name}.{audio_output_format}")
        result = pipe(audio_file)

        formatted_result = ""
        if "chunks" in result:
            for chunk in result["chunks"]:
                # Add safe handling for timestamps that might be None
                timestamp = chunk.get("timestamp", [None, None])
                start_time = (
                    timestamp[0]
                    if timestamp and len(timestamp) > 0 and timestamp[0] is not None
                    else 0
                )
                end_time = (
                    timestamp[1]
                    if timestamp and len(timestamp) > 1 and timestamp[1] is not None
                    else 0
                )
                text = chunk.get("text", "")
                formatted_result += f"[{start_time:.2f}s -> {end_time:.2f}s] {text}\n"
        else:
            # Handle the case where timestamps are provided differently
            for i, segment in enumerate(result.get("segments", [])):
                start = segment.get("start", 0)
                end = segment.get("end", 0)
                text = segment.get("text", "")
                formatted_result += f"[{start:.2f}s -> {end:.2f}s] {text}\n"

        transcripts[index] = formatted_result

    return transcripts
