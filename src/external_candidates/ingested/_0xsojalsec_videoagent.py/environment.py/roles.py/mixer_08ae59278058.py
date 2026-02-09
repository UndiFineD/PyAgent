# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\mixer.py
import os

from environment.agents.base import BaseTool
from pydantic import BaseModel, Field
from pydub import AudioSegment


class Mixer(BaseTool):
    """
    Mix the **audio** with the BGM
    Video files are not supported directly. If needed, first extract the audio track from your video (using an audio extraction tool).
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        bgm_path: str = Field(..., description="Path to the BGM file")
        audio_path: str = Field(
            ..., description="Audio to be mixed into the background music"
        )

    class OutputSchema(BaseModel):
        audio_path: str = Field(..., description="Path to the synthesized audio")

    def execute(self, **kwargs):

        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        bgm_path = params.bgm_path
        mix_audio_path = params.audio_path

        mixed_filename = f"mixed_{os.path.basename(mix_audio_path)}"
        mixed_dir = os.path.dirname(mix_audio_path)
        output_path = os.path.join(mixed_dir, mixed_filename)

        bgm_volume = -1

        try:
            print("Loading audio files for mixing...")
            bgm_audio = AudioSegment.from_file(bgm_path)
            vocal_audio = AudioSegment.from_file(mix_audio_path)

            bgm_audio = bgm_audio + bgm_volume
            print(f"Adjusted BGM volume by {bgm_volume} dB")

            print("Mixing audio...")
            if len(bgm_audio) < len(vocal_audio):
                repeated_bgm = bgm_audio
                while len(repeated_bgm) < len(vocal_audio):
                    repeated_bgm += bgm_audio
                repeated_bgm = repeated_bgm[: len(vocal_audio)]
                mixed_audio = vocal_audio.overlay(repeated_bgm)
            else:
                mixed_audio = bgm_audio.overlay(vocal_audio)

            print(f"Exporting mixed audio to {output_path}...")
            output_format = output_path.split(".")[-1] if "." in output_path else "wav"
            mixed_audio.export(output_path, format=output_format)

            return {"audio_path": output_path}

        except Exception as e:
            print(e)
            return
