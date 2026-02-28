# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\_videoutil\split.py
import os
import shutil
import time

import numpy as np
import scipy
from moviepy.video import fx as vfx
from moviepy.video.io.VideoFileClip import VideoFileClip
from tqdm import tqdm


def split_video(
    video_path,
    working_dir,
    segment_length,
    num_frames_per_segment,
    audio_output_format="mp3",
):
    import numpy as np
    from moviepy.audio.AudioClip import AudioArrayClip
    from scipy.io import wavfile

    unique_timestamp = str(int(time.time() * 1000))
    video_name = os.path.basename(video_path).split(".")[0]
    video_segment_cache_path = os.path.join(working_dir, "_cache", video_name)
    if os.path.exists(video_segment_cache_path):
        shutil.rmtree(video_segment_cache_path)
    os.makedirs(video_segment_cache_path, exist_ok=False)

    def create_noise_audio(duration, output_path):
        # Create white noise audio array
        sample_rate = 44100
        samples = np.random.normal(0, 0.01, (int(duration * sample_rate), 2)).astype(
            np.float32
        )
        # Apply fade in and fade out
        fade_duration = min(0.1, duration / 4)  # 100ms or quarter of duration
        fade_samples = int(fade_duration * sample_rate)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)

        # Apply fades
        samples[:fade_samples] *= fade_in[:, np.newaxis]
        samples[-fade_samples:] *= fade_out[:, np.newaxis]

        # Normalize to prevent clipping
        samples = samples / np.max(np.abs(samples)) * 0.5

        audio_clip = AudioArrayClip(samples, fps=sample_rate)
        audio_clip.write_audiofile(
            output_path, fps=sample_rate, codec="mp3", verbose=False, logger=None
        )

    segment_index = 0
    segment_index2name, segment_times_info = {}, {}
    with VideoFileClip(video_path) as video:

        total_video_length = int(video.duration)
        start_times = list(range(0, total_video_length, segment_length))
        # if the last segment is shorter than 5 seconds, we merged it to the last segment
        if len(start_times) > 1 and (total_video_length - start_times[-1]) < 5:
            start_times = start_times[:-1]

        for start in tqdm(start_times, desc=f"Spliting Video {video_name}"):
            if start != start_times[-1]:
                end = min(start + segment_length, total_video_length)
            else:
                end = total_video_length

            subvideo = video.subclip(start, end)
            subvideo_length = subvideo.duration
            frame_times = np.linspace(
                0, subvideo_length, num_frames_per_segment, endpoint=False
            )
            frame_times += start

            segment_index2name[f"{segment_index}"] = (
                f"{unique_timestamp}-{segment_index}-{start}-{end}"
            )
            segment_times_info[f"{segment_index}"] = {
                "frame_times": frame_times,
                "timestamp": (start, end),
            }

            # save audio
            audio_file_base_name = segment_index2name[f"{segment_index}"]
            audio_file = f"{audio_file_base_name}.{audio_output_format}"
            audio_path = os.path.join(video_segment_cache_path, audio_file)

            if subvideo.audio is not None:
                subaudio = subvideo.audio
                subaudio.write_audiofile(
                    audio_path, codec="mp3", verbose=False, logger=None
                )
            else:
                # Create white noise audio file
                create_noise_audio(subvideo_length, audio_path)

            segment_index += 1

    return segment_index2name, segment_times_info


def saving_video_segments(
    video_name,
    video_path,
    working_dir,
    segment_index2name,
    segment_times_info,
    error_queue,
    video_output_format="mp4",
):
    try:
        with VideoFileClip(video_path) as video:
            video_segment_cache_path = os.path.join(working_dir, "_cache", video_name)
            for index in tqdm(
                segment_index2name, desc=f"Saving Video Segments {video_name}"
            ):
                start, end = (
                    segment_times_info[index]["timestamp"][0],
                    segment_times_info[index]["timestamp"][1],
                )
                video_file = f"{segment_index2name[index]}.{video_output_format}"
                subvideo = video.subclip(start, end)
                subvideo.write_videofile(
                    os.path.join(video_segment_cache_path, video_file),
                    codec="libx264",
                    verbose=False,
                    logger=None,
                )
    except Exception as e:
        error_queue.put(f"Error in saving_video_segments:\n {str(e)}")
        raise RuntimeError
