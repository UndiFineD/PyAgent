# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\cross_talk\cross_talk_conversion.py
import json
import os

import soundfile as sf
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field


class CrossTalkConversion(BaseTool):
    """
    Application scenario: Cross talk Creating
    Convert segmented audio files into JSON timestamp format for subsequent video generation.
    If video footage needs to be added later, first call VideoConversion.
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        seg_dir: str = Field(..., description="Directory containing all segmented cross talk audio files")
        metadata_path: str = Field(..., description="File path to the metadata of the cross talk script")

    class OutputSchema(BaseModel):
        timestamp_path: str = Field(
            ...,
            description="File path storing video segment timestamps for seamless video switching during editing",
        )

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        seg_dir = params.seg_dir
        metadata_path = params.metadata_path

        chunks = []
        current_time = 0.0
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        for idx, item in enumerate(metadata):
            wav_path = os.path.join(seg_dir, f"{idx}.wav")
            try:
                metadata, samplerate = sf.read(wav_path)
                duration = len(metadata) / samplerate
                end_time = current_time + duration

                content = f"[{item['role']}] {item['text']}"

                chunks.append({"id": idx + 1, "timestamp": round(end_time, 3), "content": content})

                current_time = end_time

            except Exception as e:
                print(f"Failed to read {wav_path}: {str(e)}")
                continue

        result = {"sentence_data": {"count": len(chunks), "chunks": chunks}}

        timestamp_path = os.path.join(os.path.dirname(metadata_path), "timestamps.json")
        with open(timestamp_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return {"timestamp_path": timestamp_path}
