# Extracted from: C:\DEV\PyAgent\.external\ACTalker\eval\concate.py
"""将svd输出的视频和reference进行拼接"""

import glob
import multiprocessing
import os
import sys
from argparse import ArgumentParser
from contextlib import contextmanager

import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip, VideoFileClip
from tqdm import tqdm


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(os.devnull, "w") as fnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def op_concate(opt, video):
    video_path = os.path.join(opt.video_dir, video)
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()

    if os.path.exists(os.path.join(opt.image_dir, video.split(".")[0] + ".png")):
        img = cv2.imread(os.path.join(opt.image_dir, video.split(".")[0] + ".png"))
        img = cv2.resize(img, frame.shape[:2])
    else:
        return

    index = 0
    save_path_list = []
    while success:
        frame = np.concatenate([img, frame], axis=1)
        save_path = os.path.join(opt.save_dir, video.split(".")[0], "%05d.png" % index)
        os.makedirs(os.path.join(opt.save_dir, video.split(".")[0]), exist_ok=True)

        cv2.imwrite(save_path, frame)
        save_path_list.append(save_path)
        success, frame = cap.read()
        index += 1

    with suppress_stdout_stderr():
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        clip = ImageSequenceClip(save_path_list, fps=25)
        clip = clip.set_duration(video_clip.duration)
        clip = clip.set_audio(audio_clip)
        clip = clip.subclip(0, clip.duration - 5.5)
        clip.write_videofile(
            os.path.join(opt.save_dir, video),
            codec="libx264",
            audio_codec="aac",
            verbose=False,
        )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--save_dir", default="./results/", help="path to save result videos and images"
    )
    parser.add_argument("--video_dir", default="./results/")
    parser.add_argument(
        "--image_dir",
        default="/apdcephfs_jn/share_302243908/0_public_datasets/audio-testset/image-sqare",
    )
    parser.add_argument("--model_path", default=None)
    parser.add_argument("--num", default=20, type=int)

    opt = parser.parse_args()
    if opt.model_path is not None:
        model_name = os.path.splitext(os.path.basename(opt.model_path))[0]
        opt.save_dir = os.path.join(opt.save_dir, model_name)

    pool = multiprocessing.Pool(10)
    results = []

    file_list = os.listdir(opt.video_dir)
    file_list = sorted(file_list)

    for video in tqdm(file_list[: opt.num]):
        results.append(pool.apply_async(op_concate, args=(opt, video)))

    pool.close()

    for result in tqdm(results):
        result.get()
    pool.join()


if __name__ == "__main__":
    main()
