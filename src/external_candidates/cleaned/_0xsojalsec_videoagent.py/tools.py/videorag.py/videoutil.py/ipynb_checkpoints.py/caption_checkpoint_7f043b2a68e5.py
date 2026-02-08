# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\_videoutil\.ipynb_checkpoints\caption-checkpoint.py
import os

import numpy as np
import torch
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer


def encode_video(video, frame_times):
    frames = []
    for t in frame_times:
        frames.append(video.get_frame(t))
    frames = np.stack(frames, axis=0)
    frames = [Image.fromarray(v.astype("uint8")).resize((1280, 720)) for v in frames]
    return frames


def segment_caption(
    video_name,
    video_path,
    segment_index2name,
    transcripts,
    segment_times_info,
    caption_result,
    error_queue,
):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up two levels to reach the tools directory
        # From _videoutil to videorag to tools
        tools_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

        # Path to the MiniCPM model
        model_path = os.path.join(tools_dir, "MiniCPM-V-2_6-int4")

        if not os.path.exists(model_path):
            print(f"Warning: Local model not found at {model_path}, falling back to Hugging Face")
        else:
            model_id = model_path
            print(f"Using local MiniCPM model from: {model_path}")

        model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        model.eval()

        with VideoFileClip(video_path) as video:
            for index in tqdm(segment_index2name, desc=f"Captioning Video {video_name}"):
                frame_times = segment_times_info[index]["frame_times"]
                video_frames = encode_video(video, frame_times)
                segment_transcript = transcripts[index]
                query = f"The transcript of the current video:\n{segment_transcript}.\nNow provide a scene description of the video in English, and provide a detailed description of every character's appearance (eg. Age, gender, clothing, appearance, actions)."
                msgs = [{"role": "user", "content": video_frames + [query]}]
                params = {}
                params["use_image_id"] = False
                params["max_slice_nums"] = 2
                segment_caption = model.chat(image=None, msgs=msgs, tokenizer=tokenizer, **params)
                caption_result[index] = segment_caption.replace("\n", "").replace("<|endoftext|>", "")
                torch.cuda.empty_cache()
    except Exception as e:
        error_queue.put(f"Error in segment_caption:\n {str(e)}")
        raise RuntimeError


def merge_segment_information(segment_index2name, segment_times_info, transcripts):
    inserting_segments = {}
    for index in segment_index2name:
        inserting_segments[index] = {"content": None, "time": None}
        segment_name = segment_index2name[index]
        inserting_segments[index]["time"] = "-".join(segment_name.split("-")[-2:])
        inserting_segments[index]["transcript"] = transcripts[index]
        inserting_segments[index]["frame_times"] = segment_times_info[index]["frame_times"].tolist()
    return inserting_segments
