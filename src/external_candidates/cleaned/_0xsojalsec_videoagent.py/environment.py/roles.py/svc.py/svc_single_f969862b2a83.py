# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\svc\svc_single.py
import json
import os
import re

import librosa
import numpy as np
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field
from pydub import AudioSegment

from tools.DiffSinger.diff import run_diffsinger


class SVCSingle(BaseTool):
    """
    Application scenario: Music cover (maintaining original melody with modified lyrics and vocal timbre alteration
    Split the adapted lyrics into segments, then synthesize each segment with the default vocal singing voice
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        adapted_lyrics: str = Field(..., description="String of the adapted lyrics")
        analysis_path: str = Field(..., description="File path to the MIDI analysis results")
        name: str = Field(..., description="Name of the song")

    class OutputSchema(BaseModel):
        audio_path: str = Field(..., description="File path to vocal singing audio")

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")
        analysis_path = params.analysis_path

        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis = json.load(f)

        inp = {
            "text": params.adapted_lyrics,
            "notes": analysis["notes"],
            "notes_duration": analysis["notes_duration"],
            "input_type": "word",
        }

        text_list, notes_list, notes_duration_list = self._split_single_annotation(inp)

        name = params.name
        source_vocal_song = self._generate_audio_segments_batch(name, text_list, notes_list, notes_duration_list)

        # 创建返回消息
        return {"audio_path": source_vocal_song}

    def _split_single_annotation(self, data):
        text = data["text"]
        notes = data["notes"].split(" | ")
        notes_duration = data["notes_duration"].split(" | ")

        # 去掉可能的空字符串
        notes = [n for n in notes if n]
        notes_duration = [d for d in notes_duration if d]

        # 1. 先用 "AP" 分割 text
        segments = re.split("(AP)", text)
        filtered_segments = [seg for seg in segments if seg]

        # 2. 对非 "AP" 的 segment 按单字拆分
        final_segments = []
        for seg in filtered_segments:
            if seg == "AP":
                final_segments.append("AP")
            else:
                final_segments.extend(list(seg))

        # 3. 生成对齐的 notes 和 duration
        notes_list = []
        notes_duration_list = []
        current_index = 0

        for seg in final_segments:
            if seg == "AP":
                if current_index < len(notes) and notes[current_index] == "rest":
                    notes_list.append(notes[current_index])
                    notes_duration_list.append(notes_duration[current_index])
                    current_index += 1
                else:
                    raise ValueError(f"Expected 'rest' at index {current_index}")
            else:
                if current_index < len(notes) and notes[current_index] != "rest":
                    notes_list.append(notes[current_index])
                    notes_duration_list.append(notes_duration[current_index])
                    current_index += 1
                else:
                    raise ValueError(f"Expected note at index {current_index}")
        return final_segments, notes_list, notes_duration_list

    def _create_segment(self, idx, text_list, notes_list, notes_duration_list):
        return {
            "text": text_list[idx],
            "notes": notes_list[idx],
            "notes_duration": notes_duration_list[idx],
            "input_type": "word",
        }

    def _phase_vocoder_stretch(self, audio_array, sr, target_duration_sec):
        """精确拉伸音频到目标时长（采样数级精确）"""
        current_duration = len(audio_array) / sr
        target_samples = int(target_duration_sec * sr)

        # 方法1：相位声码器（适合语音，但可能有微小误差）
        stretch_factor = current_duration / target_duration_sec
        stretched = librosa.effects.time_stretch(audio_array, rate=stretch_factor)

        # 方法2：采样数级精确裁剪/补零（强制匹配）
        if len(stretched) > target_samples:
            stretched = stretched[:target_samples]  # 裁剪多余部分
        else:
            # 不足时补零（保持语调不变）
            padded = np.zeros(target_samples)
            padded[: len(stretched)] = stretched
            stretched = padded

        return stretched

    def _generate_audio_segments(self, name, text_list, notes_list, notes_duration_list):
        """生成完整音频并返回最终路径（精确时长控制版）"""
        new_name = f"{name}_cover"
        cover_dir = "dataset/mad_svc/cover"
        os.makedirs("dataset/mad_svc/lyrics_annotation", exist_ok=True)

        # 初始化音频（统一使用44.1kHz采样率）
        combined_audio = AudioSegment.silent(duration=0, frame_rate=44100)
        total_expected_duration = 0
        sr = 44100  # 固定采样率

        for i in range(len(text_list)):
            segment_type = "AP" if text_list[i] == "AP" else "Voice"
            target_duration_sec = float(notes_duration_list[i])
            total_expected_duration += target_duration_sec

            if segment_type == "AP":
                # 精确静音生成（采样点级别精确）
                silence_samples = int(round(target_duration_sec * sr))
                silence = AudioSegment(
                    data=np.zeros(silence_samples, dtype=np.int16).tobytes(),
                    sample_width=2,
                    frame_rate=sr,
                    channels=1,
                )
                combined_audio += silence
                print(
                    f"Silence Segment {i}: target={target_duration_sec:.3f}s, "
                    f"actual={len(silence) / 1000:.3f}s, samples={silence_samples}"
                )

            else:
                # 生成语音片段
                segment = self._create_segment(i, text_list, notes_list, notes_duration_list)
                segment_name = f"{new_name}_part_{i}"
                inp_path = os.path.join("dataset/mad_svc/lyrics_annotation", f"{segment_name}.json")

                with open(inp_path, "w", encoding="utf-8") as f:
                    json.dump(segment, f, ensure_ascii=False, indent=2)

                try:
                    # 调用DiffSinger生成原始音频
                    run_diffsinger(input_dir="../../" + inp_path, save_name=segment_name)
                    seg_audio_path = os.path.join(cover_dir, f"{segment_name}.wav")

                    if not os.path.exists(seg_audio_path):
                        raise FileNotFoundError(f"生成的音频文件 {seg_audio_path} 不存在")

                    # 加载音频并统一采样率
                    audio_array, _ = librosa.load(seg_audio_path, sr=sr, mono=True)

                    # 时间拉伸（仅在必要时）
                    current_duration = len(audio_array) / sr
                    if not np.isclose(current_duration, target_duration_sec, atol=0.01):
                        stretch_factor = current_duration / target_duration_sec
                        audio_array = librosa.effects.time_stretch(audio_array, rate=stretch_factor)

                    # 转换为AudioSegment（原始长度，不做截断）
                    audio_segment = AudioSegment(
                        data=(np.clip(audio_array, -1.0, 1.0) * 32767).astype(np.int16).tobytes(),
                        sample_width=2,
                        frame_rate=sr,
                        channels=1,
                    )

                    # 强制时长对齐（毫秒级精确操作）
                    target_ms = int(round(target_duration_sec * 1000))
                    actual_ms = len(audio_segment)

                    if actual_ms != target_ms:
                        print(
                            f"Adjusting segment {i}: "
                            f"target={target_ms}ms ({target_duration_sec:.3f}s), "
                            f"actual={actual_ms}ms ({actual_ms / 1000:.3f}s)"
                        )

                        if actual_ms < target_ms:
                            # 补静音
                            silence = AudioSegment.silent(duration=target_ms - actual_ms, frame_rate=sr)
                            audio_segment += silence
                        else:
                            # 截断
                            audio_segment = audio_segment[:target_ms]

                        print(f"After adjustment: {len(audio_segment)}ms (error={len(audio_segment) - target_ms}ms)")

                    # 最终验证
                    final_error_ms = len(audio_segment) - target_ms
                    if abs(final_error_ms) > 1:
                        print(f"Warning: Segment {i} still has error: {final_error_ms}ms")

                    combined_audio += audio_segment

                finally:
                    # 清理临时文件
                    for path in [inp_path, seg_audio_path]:
                        if os.path.exists(path):
                            os.remove(path)

        # 最终时长验证
        total_actual_duration = len(combined_audio) / 1000
        print(f"\nFinal duration check:")
        print(f"Expected: {total_expected_duration:.3f}s")
        print(f"Actual:   {total_actual_duration:.3f}s")
        print(f"Error:    {total_actual_duration - total_expected_duration:.3f}s")

        # 保存结果
        final_output_path = os.path.join(cover_dir, f"{new_name}.wav")
        combined_audio.export(final_output_path, format="wav")
        return final_output_path

    def _create_segment_with_min_duration(
        self,
        start_idx,
        text_list,
        notes_list,
        notes_duration_list,
        threshold_duration=0.15,
        min_duration=0.5,
    ):
        duration = float(notes_duration_list[start_idx])
        segment = {
            "text": text_list[start_idx],
            "notes": notes_list[start_idx],
            "notes_duration": notes_duration_list[start_idx],
            "input_type": "word",
        }
        if segment["text"] == "AP":
            return segment, duration

        if duration < threshold_duration:
            idx = start_idx + 1
            while duration < min_duration and idx < len(text_list) and text_list[idx] != "AP":
                duration += float(notes_duration_list[idx])
                segment["text"] += text_list[idx]
                segment["notes"] += " | " + notes_list[idx]
                segment["notes_duration"] += " | " + notes_duration_list[idx]
                idx += 1

        return segment, duration

    def _generate_audio_segments_batch(self, name, text_list, notes_list, notes_duration_list):
        """生成完整音频并返回最终路径（精确时长控制版）"""
        new_name = f"{name}_cover"
        cover_dir = "dataset/mad_svc/cover"
        os.makedirs("dataset/mad_svc/lyrics_annotation", exist_ok=True)

        tmp_dir = "dataset/mad_svc/tmp"
        os.makedirs(tmp_dir, exist_ok=True)

        # 切片
        segments = []
        start_idx = 0
        while start_idx < len(text_list):
            segment, duration = self._create_segment_with_min_duration(
                start_idx, text_list, notes_list, notes_duration_list
            )
            if segment["text"] == "AP":
                end_idx = start_idx + 1
            else:
                end_idx = start_idx + len(segment["text"])
            segments.append(
                {
                    "segment": segment,
                    "start": start_idx,
                    "end": end_idx,
                    "duration": duration,
                }
            )
            # 生成临时文件
            start_idx_str = str(start_idx).zfill(4)
            end_idx_str = str(end_idx).zfill(4)
            if segment["text"] != "AP":
                with open(
                    os.path.join(tmp_dir, f"{new_name}_part_{start_idx_str}-{end_idx_str}.json"),
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(segment, f, ensure_ascii=False, indent=2)
            start_idx = end_idx

        # 按切片生成音频
        try:
            run_diffsinger(input_dir=tmp_dir)
            pass
        except Exception as e:
            print(f"Error during DiffSinger execution: {e}")
            return None
        # finally:
        #     pass
        # 清理临时文件
        # for path in os.listdir(tmp_dir):
        #     os.remove(os.path.join(tmp_dir, path))

        # 合并音频
        combined_audio = AudioSegment.silent(duration=0, frame_rate=44100)
        total_expected_duration = 0
        sr = 44100

        for i, segment in enumerate(segments):
            segment_type = "AP" if segment["segment"]["text"] == "AP" else "Voice"
            target_duration_sec = segment["duration"]
            total_expected_duration += target_duration_sec

            if segment_type == "AP":
                # 精确静音生成（采样点级别精确）
                silence_samples = int(round(target_duration_sec * sr))
                silence = AudioSegment(
                    data=np.zeros(silence_samples, dtype=np.int16).tobytes(),
                    sample_width=2,
                    frame_rate=sr,
                    channels=1,
                )
                combined_audio += silence
                print(
                    f"Silence Segment {i}: target={target_duration_sec:.3f}s, "
                    f"actual={len(silence) / 1000:.3f}s, samples={silence_samples}"
                )

            else:
                # 读取生成的音频
                start_idx_str = str(segment["start"]).zfill(4)
                end_idx_str = str(segment["end"]).zfill(4)
                segment_wav_name = f"{new_name}_part_{start_idx_str}-{end_idx_str}.wav"
                seg_audio_path = os.path.join(cover_dir, segment_wav_name)
                if not os.path.exists(seg_audio_path):
                    raise FileNotFoundError(f"生成的音频文件 {seg_audio_path} 不存在")

                audio_array, _ = librosa.load(seg_audio_path, sr=sr, mono=True)

                # 删除临时文件
                # os.remove(seg_audio_path)

                # 时间拉伸（仅在必要时）
                current_duration = len(audio_array) / sr
                if not np.isclose(current_duration, target_duration_sec, atol=0.01):
                    stretch_factor = current_duration / target_duration_sec
                    audio_array = librosa.effects.time_stretch(audio_array, rate=stretch_factor)

                # 转换为AudioSegment（原始长度，不做截断）
                audio_segment = AudioSegment(
                    data=(np.clip(audio_array, -1.0, 1.0) * 32767).astype(np.int16).tobytes(),
                    sample_width=2,
                    frame_rate=sr,
                    channels=1,
                )

                # 强制时长对齐（毫秒级精确操作）
                target_ms = int(round(target_duration_sec * 1000))
                actual_ms = len(audio_segment)

                if actual_ms != target_ms:
                    print(
                        f"Adjusting segment {i}: "
                        f"target={target_ms}ms ({target_duration_sec:.3f}s), "
                        f"actual={actual_ms}ms ({actual_ms / 1000:.3f}s)"
                    )

                    if actual_ms < target_ms:
                        # 补静音
                        silence = AudioSegment.silent(duration=target_ms - actual_ms, frame_rate=sr)
                        audio_segment += silence
                    else:
                        # 截断
                        audio_segment = audio_segment[:target_ms]

                    print(f"After adjustment: {len(audio_segment)}ms (error={len(audio_segment) - target_ms}ms)")

                # 最终验证
                final_error_ms = len(audio_segment) - target_ms
                if abs(final_error_ms) > 1:
                    print(f"Warning: Segment {i} still has error: {final_error_ms}ms")

                combined_audio += audio_segment

        # 最终时长验证
        total_actual_duration = len(combined_audio) / 1000
        print(f"\nFinal duration check:")
        print(f"Expected: {total_expected_duration:.3f}s")
        print(f"Actual:   {total_actual_duration:.3f}s")
        print(f"Error:    {total_actual_duration - total_expected_duration:.3f}s")

        # 保存结果
        final_output_path = os.path.join(cover_dir, f"{new_name}.wav")
        combined_audio.export(final_output_path, format="wav")
        return final_output_path
