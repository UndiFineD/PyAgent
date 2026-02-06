# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\_videoutil\caption.py
import base64
import io
import os

import numpy as np
from environment.config.llm import gemini
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image
from tqdm import tqdm


def encode_video(video, frame_times):
    frames = []
    for t in frame_times:
        frames.append(video.get_frame(t))
    frames = np.stack(frames, axis=0)
    frames = [Image.fromarray(v.astype("uint8")).resize((1280, 720)) for v in frames]
    return frames


def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def frames_to_description(video_frames):
    """Convert video frames to base64 format for Gemini API"""
    frame_data = []
    for i, frame in enumerate(video_frames):
        base64_image = image_to_base64(frame)
        frame_data.append({"frame_number": i + 1, "image_data": base64_image})
    return frame_data


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
        with VideoFileClip(video_path) as video:
            for index in tqdm(
                segment_index2name, desc=f"Captioning Video {video_name}"
            ):
                frame_times = segment_times_info[index]["frame_times"]
                video_frames = encode_video(video, frame_times)

                # Get frame data with base64 images
                frame_data = frames_to_description(video_frames)

                transcript_context = (
                    transcripts[index]
                    if transcripts[index].strip()
                    else "No transcript available"
                )

                # Create content array with text and images
                content = [
                    {
                        "type": "text",
                        "text": f"""You are analyzing a video segment. Here's the available information:

                Transcript: {transcript_context}
                
                I'm providing {len(video_frames)} frames from this video segment. Based on the transcript and these visual frames, provide a detailed scene description focusing on:
                - Visual elements present in the video
                - Actions and movements occurring
                - Setting and environment details
                - Characters or objects visible
                - Overall scene composition and mood
                
                Provide a comprehensive description without including unrelated information.
                
                ##############Example Output##############
                
                A bustling city street with people walking, cars passing by, and tall buildings in the background. The scene captures the energy of urban life with pedestrians crossing the road, cyclists navigating through traffic.
                """,
                    }
                ]

                # Add each frame as an image input
                for frame_info in frame_data:
                    content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{frame_info['image_data']}"
                            },
                        }
                    )

                try:
                    response = gemini(
                        user=content  # Send the content array with text + images
                    )

                    segment_caption_text = response.choices[0].message.content
                    caption_result[index] = segment_caption_text.replace(
                        "\n", ""
                    ).replace("<|endoftext|>", "")

                except Exception as api_error:
                    print(f"Gemini API error for segment {index}: {str(api_error)}")
                    fallback_caption = (
                        f"Video segment containing: {transcript_context}"
                        if transcript_context != "No transcript available"
                        else "Video segment with visual content"
                    )
                    caption_result[index] = fallback_caption

    except Exception as e:
        error_queue.put(f"Error in segment_caption:\n {str(e)}")
        raise RuntimeError


def merge_segment_information(
    segment_index2name, segment_times_info, transcripts, captions
):
    inserting_segments = {}
    for index in segment_index2name:
        inserting_segments[index] = {"content": None, "time": None}
        segment_name = segment_index2name[index]
        inserting_segments[index]["time"] = "-".join(segment_name.split("-")[-2:])
        inserting_segments[index][
            "content"
        ] = f"Caption:\n{captions[index]}"  # \nTranscript:\n{transcripts[index]}\n\n"
        inserting_segments[index]["transcript"] = transcripts[index]
        inserting_segments[index]["frame_times"] = segment_times_info[index][
            "frame_times"
        ].tolist()
    return inserting_segments
