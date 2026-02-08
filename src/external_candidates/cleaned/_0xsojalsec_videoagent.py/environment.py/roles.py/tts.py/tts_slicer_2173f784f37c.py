# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\tts\tts_slicer.py
import json
import math
import os

import librosa
import numpy as np
import soundfile as sf
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field


class TTSSlicer(BaseTool):
    """
    Application scenario: A reworded version of the original video
    Slice the audio into segments. The audio segments often need to be transcribed afterward.
    """

    class InputSchema(BaseTool.BaseInputSchema):
        audio_path: str = Field(..., description="File path to the audio track of the video")

    class OutputSchema(BaseModel):
        status: str = Field(..., description="Execution status (success/error)")

    def __init__(
        self,
        min_duration=6.0,
        max_duration=8.0,
        min_silence_duration=0.5,
        top_db=-35,
        hop_length=10,
        max_silence_kept=0.3,
        merge_short=False,
    ):
        super().__init__()
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.min_silence_duration = min_silence_duration
        self.top_db = top_db
        self.hop_length = hop_length
        self.max_silence_kept = max_silence_kept
        self.merge_short = merge_short

    class _Slicer:
        def __init__(
            self,
            sr: int,
            threshold: float,
            min_length: int,
            min_interval: int,
            hop_size: int,
            max_sil_kept: int,
        ):
            if not min_length >= min_interval >= hop_size:
                raise ValueError("The condition to be satisfied is：min_length >= min_interval >= hop_size")

            if not max_sil_kept >= hop_size:
                raise ValueError("The condition to be satisfied is: max_sil_kept >= hop_size")

            min_interval = sr * min_interval // 1000
            self.sr = sr
            self.threshold = 10 ** (threshold / 20.0)
            self.hop_size = round(sr * hop_size / 1000)
            self.win_size = min(round(min_interval), 4 * self.hop_size)
            self.min_length = round(sr * min_length / 1000 / self.hop_size)
            self.min_interval = round(min_interval / self.hop_size)
            self.max_sil_kept = round(sr * max_sil_kept / 1000 / self.hop_size)

        def _apply_slice(self, waveform, begin, end):
            start_idx = begin * self.hop_size
            end_idx = min(waveform.shape[-1], end * self.hop_size)

            sliced = waveform[..., start_idx:end_idx] if len(waveform.shape) > 1 else waveform[start_idx:end_idx]

            return {
                "audio": sliced,
                "start": start_idx / self.sr,
                "end": end_idx / self.sr,
            }

        def slice(self, waveform):
            samples = waveform.mean(axis=0) if len(waveform.shape) > 1 else waveform
            total_samples = samples.shape[0]

            if total_samples <= self.min_length * self.hop_size:
                return [{"audio": waveform, "start": 0.0, "end": total_samples / self.sr}]

            rms_list = librosa.feature.rms(y=samples, frame_length=self.win_size, hop_length=self.hop_size).squeeze(0)

            sil_tags = []
            silence_start = None
            clip_start = 0

            for i, rms in enumerate(rms_list):
                if rms < self.threshold:
                    if silence_start is None:
                        silence_start = i
                    continue

                if silence_start is None:
                    continue

                is_leading_silence = silence_start == 0 and i > self.max_sil_kept
                need_slice_middle = i - silence_start >= self.min_interval and i - clip_start >= self.min_length

                if not is_leading_silence and not need_slice_middle:
                    silence_start = None
                    continue

                if i - silence_start <= self.max_sil_kept:
                    pos = rms_list[silence_start : i + 1].argmin() + silence_start
                    sil_tags.append((pos, pos) if silence_start != 0 else (0, pos))
                    clip_start = pos
                elif i - silence_start <= self.max_sil_kept * 2:
                    pos = (
                        rms_list[i - self.max_sil_kept : silence_start + self.max_sil_kept + 1].argmin()
                        + i
                        - self.max_sil_kept
                    )
                    pos_l = rms_list[silence_start : silence_start + self.max_sil_kept + 1].argmin() + silence_start
                    pos_r = rms_list[i - self.max_sil_kept : i + 1].argmin() + i - self.max_sil_kept

                    if silence_start == 0:
                        sil_tags.append((0, pos_r))
                        clip_start = pos_r
                    else:
                        sil_tags.append((min(pos_l, pos), max(pos_r, pos)))
                        clip_start = max(pos_r, pos)
                else:
                    pos_l = rms_list[silence_start : silence_start + self.max_sil_kept + 1].argmin() + silence_start
                    pos_r = rms_list[i - self.max_sil_kept : i + 1].argmin() + i - self.max_sil_kept
                    sil_tags.append((pos_l, pos_r) if silence_start != 0 else (0, pos_r))
                    clip_start = pos_r

                silence_start = None

            total_frames = len(rms_list)
            if silence_start is not None and total_frames - silence_start >= self.min_interval:
                silence_end = min(total_frames, silence_start + self.max_sil_kept)
                pos = rms_list[silence_start : silence_end + 1].argmin() + silence_start
                sil_tags.append((pos, total_frames + 1))

            if not sil_tags:
                return [{"audio": waveform, "start": 0.0, "end": total_samples / self.sr}]

            chunks = []
            if sil_tags[0][0] > 0:
                chunks.append(self._apply_slice(waveform, 0, sil_tags[0][0]))

            for i in range(len(sil_tags) - 1):
                chunks.append(self._apply_slice(waveform, sil_tags[i][1], sil_tags[i + 1][0]))

            if sil_tags[-1][1] < total_frames:
                chunks.append(self._apply_slice(waveform, sil_tags[-1][1], total_frames))

            return chunks

    def _merge_short_chunks(self, chunks):
        merged = []
        buffer = []
        current_start = 0.0
        current_duration = 0.0

        for chunk in chunks:
            chunk_duration = chunk["end"] - chunk["start"]

            if current_duration + chunk_duration > self.max_duration and buffer:
                merged.append(
                    {
                        "audio": np.concatenate([c["audio"] for c in buffer], axis=-1),
                        "start": current_start,
                        "end": current_start + current_duration,
                    }
                )
                buffer = [chunk]
                current_start = chunk["start"]
                current_duration = chunk_duration
            else:
                if not buffer:
                    current_start = chunk["start"]
                buffer.append(chunk)
                current_duration += chunk_duration

        if buffer:
            merged.append(
                {
                    "audio": np.concatenate([c["audio"] for c in buffer], axis=-1),
                    "start": current_start,
                    "end": current_start + current_duration,
                }
            )

        return merged

    def _slice_by_max_duration(self, chunk, rate):
        audio = chunk["audio"]
        start = chunk["start"]
        total_samples = audio.shape[-1] if len(audio.shape) > 1 else len(audio)
        max_samples = math.ceil(self.max_duration * rate)

        if total_samples <= max_samples:
            return [chunk]

        chunks = []
        n_chunks = math.ceil(total_samples / max_samples)
        chunk_size = math.ceil(total_samples / n_chunks)

        for i in range(0, total_samples, chunk_size):
            end_sample = min(i + chunk_size, total_samples)
            audio_slice = audio[..., i:end_sample] if len(audio.shape) > 1 else audio[i:end_sample]

            chunks.append(
                {
                    "audio": audio_slice,
                    "start": start + i / rate,
                    "end": start + end_sample / rate,
                }
            )

        return chunks

    def slice(self, audio, rate):
        """
        切片音频数据（带精确时间戳）

        :param audio: 输入音频数组（单声道或多声道）
        :param rate: 采样率
        :return: 生成包含时间戳的字典 {
            "audio": np.ndarray,
            "start": float (秒),
            "end": float (秒)
        }
        """
        if audio.size == 0:
            return

        slicer = self._Slicer(
            sr=rate,
            threshold=self.top_db,
            min_length=int(self.min_duration * 1000),
            min_interval=int(self.min_silence_duration * 1000),
            hop_size=self.hop_length,
            max_sil_kept=int(self.max_silence_kept * 1000),
        )

        # 初始静音切片
        chunks = slicer.slice(audio)

        # 合并短片段
        if self.merge_short:
            chunks = self._merge_short_chunks(chunks, rate)

        # 二次最大时长切片
        for chunk in chunks:
            for sub_chunk in self._slice_by_max_duration(chunk, rate):
                yield sub_chunk

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        audio_path = params.audio_path
        slice_dir = os.path.splitext(audio_path)[0]
        os.makedirs(slice_dir, exist_ok=True)
        flat_layout = False
        save_metadata = True

        audio, rate = librosa.load(audio_path, sr=None, mono=False)
        if audio.ndim == 1:
            audio = audio[np.newaxis, :]

        metadata = []
        base_name = os.path.splitext(os.path.basename(audio_path))[0]

        for idx, chunk in enumerate(self.slice(audio, rate)):
            filename = f"{base_name}_{idx:04d}.wav" if flat_layout else f"{idx:04d}.wav"
            output_path = os.path.join(slice_dir, filename)

            sf.write(
                output_path,
                chunk["audio"].T if len(chunk["audio"].shape) > 1 else chunk["audio"],
                rate,
            )
            metadata.append(
                {
                    "file": filename,  # Changed from relative_to to just filename
                    "start": round(chunk["start"], 3),
                    "end": round(chunk["end"], 3),
                    "duration": round(chunk["end"] - chunk["start"], 3),
                }
            )

        # Save metadata
        result = {"metadata": metadata}
        if save_metadata:
            json_path = os.path.join(slice_dir, "metadata.json")
            with open(json_path, "w") as f:
                json.dump(metadata, f, indent=2)
            result["metadata_file"] = json_path

        return {
            "status": "success",
        }
