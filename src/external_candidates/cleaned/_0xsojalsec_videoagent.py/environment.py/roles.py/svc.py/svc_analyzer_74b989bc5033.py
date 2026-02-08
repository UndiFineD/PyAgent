# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\svc\svc_analyzer.py
import json
import os

import mido
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field


def note_to_name(note_number):
    """将MIDI音符号转换为音名"""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = note_number // 12 - 1
    note = notes[note_number % 12]
    return f"{note}{octave}"


def get_tempo_changes(mid):
    """获取所有tempo变化点"""
    tempo_changes = []
    # 默认tempo
    default_tempo = 500000
    for track in mid.tracks:
        track_time = 0
        for msg in track:
            track_time += msg.time
            if msg.type == "set_tempo":
                tempo_changes.append({"time": track_time, "tempo": msg.tempo})
    # 按时间排序
    tempo_changes.sort(key=lambda x: x["time"])
    # 如果一开始没有tempo，就插入默认tempo
    if not tempo_changes or tempo_changes[0]["time"] > 0:
        tempo_changes.insert(0, {"time": 0, "tempo": default_tempo})
    return tempo_changes


def ticks_to_seconds(start_ticks, duration_ticks, tempo_changes, ticks_per_beat):
    """将tick转换为秒数，考虑tempo变化"""
    end_ticks = start_ticks + duration_ticks
    duration_seconds = 0
    current_ticks = start_ticks

    for i in range(len(tempo_changes)):
        next_change_ticks = tempo_changes[i + 1]["time"] if i + 1 < len(tempo_changes) else float("inf")
        current_tempo = tempo_changes[i]["tempo"]

        if current_ticks >= end_ticks:
            break

        segment_end_ticks = min(end_ticks, next_change_ticks)
        segment_duration_ticks = segment_end_ticks - current_ticks

        # 转换这段时间为秒数
        duration_seconds += (segment_duration_ticks * current_tempo) / (ticks_per_beat * 1000000)
        current_ticks = segment_end_ticks

    return duration_seconds


def count_actual_notes(notes_str):
    """计算实际的音符数量（不包括休止符）"""
    notes = notes_str.split(" | ")
    return sum(1 for note in notes if note != "rest")


def analyze_midi(midi_path, lyrics, output_path):
    try:
        mid = mido.MidiFile(midi_path)
        track_results = {}
        tempo_changes = get_tempo_changes(mid)

        print("\nTempo changes:")
        for tc in tempo_changes:
            bpm = 60000000 / tc["tempo"]
            print(f"At tick {tc['time']}: {bpm:.2f} BPM")

        for track_idx, track in enumerate(mid.tracks):
            track_name = track.name if track.name else f"Track {track_idx}"
            notes_list = []
            duration_list = []

            notes = []
            current_time = 0
            current_notes = {}
            last_note_end = 0

            for msg in track:
                current_time += msg.time

                if msg.type == "note_on" and msg.velocity > 0:
                    if current_time - last_note_end > mid.ticks_per_beat / 8:
                        rest_duration = current_time - last_note_end
                        notes.append(
                            {
                                "note": "rest",
                                "start": last_note_end,
                                "duration": rest_duration,
                            }
                        )
                    current_notes[msg.note] = {
                        "start": current_time,
                        "velocity": msg.velocity,
                    }

                elif (msg.type == "note_off") or (msg.type == "note_on" and msg.velocity == 0):
                    if msg.note in current_notes:
                        start_time = current_notes[msg.note]["start"]
                        duration = current_time - start_time
                        notes.append(
                            {
                                "note": msg.note,
                                "start": start_time,
                                "duration": duration,
                            }
                        )
                        last_note_end = current_time
                        del current_notes[msg.note]

            notes.sort(key=lambda x: x["start"])

            current_time = 0
            current_group = []
            current_duration = 0

            for note in notes:
                if not current_group or abs(note["start"] - current_time) < 0.01:
                    current_group.append(note)
                    current_duration = max(current_duration, note["duration"])
                else:
                    if current_group[0]["note"] == "rest":
                        notes_list.append("rest")
                    else:
                        note_names = " ".join([note_to_name(n["note"]) for n in current_group])
                        notes_list.append(note_names)

                    duration_seconds = ticks_to_seconds(
                        current_time,
                        current_duration,
                        tempo_changes,
                        mid.ticks_per_beat,
                    )
                    duration_list.append(f"{duration_seconds:.6f}")

                    current_time = note["start"]
                    current_group = [note]
                    current_duration = note["duration"]

            if current_group:
                if current_group[0]["note"] == "rest":
                    notes_list.append("rest")
                else:
                    note_names = " ".join([note_to_name(n["note"]) for n in current_group])
                    notes_list.append(note_names)

                duration_seconds = ticks_to_seconds(current_time, current_duration, tempo_changes, mid.ticks_per_beat)
                duration_list.append(f"{duration_seconds:.6f}")

            if notes_list:
                track_results[track_name] = {
                    "notes": " | ".join(notes_list),
                    "notes_duration": " | ".join(duration_list),
                }

        print(f"\nMIDI文件共有 {len(mid.tracks)} 个轨道")

        for track_name, result in track_results.items():
            actual_notes_count = count_actual_notes(result["notes"])
            print(track_name)
            if actual_notes_count == len(lyrics):
                print(f"\n=== {track_name} ===")
                print(f"实际音符数量（不含休止符）: {actual_notes_count}")
                print(f"歌词字数: {len(lyrics)}")

                processed_lyrics = []
                current_lyric_index = 0
                notes_split = result["notes"].split(" | ")

                for note_str in notes_split:
                    if note_str == "rest":
                        processed_lyrics.append("AP")
                    else:
                        if current_lyric_index < len(lyrics):
                            processed_lyrics.append(lyrics[current_lyric_index])
                            current_lyric_index += 1

                print("\n插入后的歌词：")
                print("".join(processed_lyrics))

                print("\nNotes:")
                print(result["notes"])
                print("\nDurations (seconds):")
                print(result["notes_duration"])

                output_data = {
                    "text": "".join(processed_lyrics),
                    "notes": result["notes"],
                    "notes_duration": result["notes_duration"],
                    "input_type": "word",
                }

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)

                return result

    except Exception as e:
        print(f"Error analyzing MIDI file: {str(e)}")
        return


class SVCAnalyzer(BaseTool):
    """
    Application scenario: Music cover (maintaining original melody with modified lyrics and vocal timbre alteration
    Analyze the original song's MIDI file to extract information such as notes, note durations, etc.
    """

    class InputSchema(BaseTool.BaseInputSchema):
        midi_path: str = Field(..., description="File path to the MIDI format of the original song")
        lyrics_path: str = Field(..., description="File path to the lyrics of the original song")

    class OutputSchema(BaseModel):
        name: str = Field(..., description="Name of the song")
        analysis_path: str = Field(..., description="File path to the MIDI analysis results")

    def __init__(self):
        super().__init__()

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        midi_path = params.midi_path
        lyrics_path = params.lyrics_path

        if not midi_path.endswith(".mid"):
            return

        if not lyrics_path.endswith(".txt"):
            return

        name = os.path.splitext(os.path.basename(lyrics_path))[0]
        try:
            with open(lyrics_path, "r", encoding="utf-8") as f:
                lyrics = f.read()
        except Exception as e:
            print(e)
            return

        try:
            analysis_dir = os.path.join(os.path.dirname(midi_path), "analysis")
            os.makedirs(analysis_dir, exist_ok=True)
            analysis_path = os.path.join(analysis_dir, f"{name}.json")
            analyze_midi(midi_path, lyrics, analysis_path)

            return {
                "name": f"{name}",
                "analysis_path": f"{analysis_path}",
            }

        except Exception as e:
            print(e)
            return
