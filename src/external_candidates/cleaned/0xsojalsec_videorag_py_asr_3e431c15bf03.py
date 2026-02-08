# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_videorag.py\videorag_algorithm.py\videorag.py\videoutil.py\asr_3e431c15bf03.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoRAG\VideoRAG-algorithm\videorag\_videoutil\asr.py

import logging

import os

import torch

from faster_whisper import WhisperModel

from tqdm import tqdm

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def speech_to_text(video_name, working_dir, segment_index2name, audio_output_format):

    model = WhisperModel("./faster-distil-whisper-large-v3")

    model.logger.setLevel(logging.WARNING)

    cache_path = os.path.join(working_dir, "_cache", video_name)

    transcripts = {}

    for index in tqdm(segment_index2name, desc=f"Speech Recognition {video_name}"):
        segment_name = segment_index2name[index]

        audio_file = os.path.join(cache_path, f"{segment_name}.{audio_output_format}")

        # if the audio file does not exist, skip it

        if not os.path.exists(audio_file):
            transcripts[index] = ""

            continue

        segments, info = model.transcribe(audio_file)

        result = ""

        for segment in segments:
            result += "[%.2fs -> %.2fs] %s\n" % (
                segment.start,
                segment.end,
                segment.text,
            )

        transcripts[index] = result

    return transcripts
