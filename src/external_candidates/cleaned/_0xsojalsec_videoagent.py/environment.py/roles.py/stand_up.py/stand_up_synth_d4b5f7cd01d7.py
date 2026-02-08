# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\stand_up\stand_up_synth.py
import json
import os

import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
from environment.agents.base import BaseTool
from environment.config.llm import deepseek
from pydantic import BaseModel, Field
from pydub import AudioSegment


class StandUpSynth(BaseTool):
    """
    Application scenario: Stand-up Comedy Creating
    Segment-by-segment stand-up comedy audio synthesis with final merge
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        script: str = Field(..., description="String of segmented stand-up comedy script")
        target_vocal_dir: str = Field(..., description="The target vocal directory for stand-up comedy synthesis.")
        reaction_dir: str = Field(
            ...,
            description="The audience reaction directory for stand-up comedy synthesis.",
        )

    class OutputSchema(BaseModel):
        audio_path: str = Field(..., description="File path to the merged stand-up comedy audio")
        seg_dir: str = Field(
            ...,
            description="Directory containing all segmented stand-up comedy audio files",
        )
        metadata_path: str = Field(..., description="File path to the metadata of the stand-up comedy script")

    def merge_audio_files(self, seg_dir, cnt):
        merged_audio = AudioSegment.silent(duration=0)

        for i in range(cnt):
            audio_file_path = os.path.join(seg_dir, f"{i}.wav")
            try:
                audio_segment = AudioSegment.from_file(audio_file_path)
                merged_audio += audio_segment
                print(f"Successfully added {audio_file_path} to the combined audio.")
            except Exception as e:
                print(f"Error loading {audio_file_path}: {str(e)}")

        parent_dir = os.path.dirname(seg_dir)
        os.makedirs(os.path.join(parent_dir, "final"), exist_ok=True)
        output_file_path = os.path.join(parent_dir, "final", "stand_up.wav")
        merged_audio.export(output_file_path, format="wav")
        abs_output_file_path = os.path.abspath(output_file_path)
        print(f"Combined audio saved to {abs_output_file_path}")

        return abs_output_file_path

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        script = params.script
        target_vocal_dir = os.path.abspath(params.target_vocal_dir)
        reaction_dir = os.path.abspath(params.reaction_dir)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "tools", "CosyVoice"))
        try:
            cosyvoice = CosyVoice2(
                "pretrained_models/CosyVoice2-0.5B",
                load_jit=False,
                load_trt=False,
                fp16=False,
            )
        except Exception as e:
            print("cosyvoice issue:", e)
            return

        cnt = 0
        results = []
        first_line = True
        seg_dir = os.path.join(os.path.dirname(target_vocal_dir), "seg")
        os.makedirs(seg_dir, exist_ok=True)

        for line in script.split("\n"):
            if not line.strip():
                continue
            if first_line:
                first_line = False
                continue
            user_prompt = f"""
            Analyze the tone, text content, and atmosphere marker of the following stand-up comedy segment:
            {line}

            Output strictly in JSON format with these rules:
            1. "tone" field must be ONLY "Natural", "Empathetic", "Confused" or "Exclamatory"
            2. "text" field contains the segment's content
            3. Add "reaction" field ONLY if there's atmosphere marker (i.e. [Laughter] or [Cheers]) behind the sentence, value must be "Laughter" or "Cheers"
            4. You should not analyze the tone and atmosphere markers of the segment yourself, but instead strictly rely on whether these markers appear in the segment.
            5. NO extra characters or explanations before/after JSON

            Example 1:
            
            {{
                "tone": "Empathetic",
                "text": "..."
            }}

            Example 2:
            {{
                "tone": "Natural",
                "text": "...",
                "reaction": "Cheers"
            }}

            Ensure the output is strictly in JSON format!
            """

            try:
                response = deepseek(user=user_prompt)
                res = response.choices[0].message.content

                if res.startswith("```json"):
                    res = res[len("```json") :]
                elif res.startswith("```"):
                    res = res[len("```") :]
                if res.endswith("```"):
                    res = res[:-3]
                res = res.strip()
                print(cnt, ":", res)

                result = json.loads(res)
                tone = result["tone"].lower()
                text = result["text"].strip()

                with open(os.path.join(target_vocal_dir, f"{tone}.lab"), "r", encoding="utf-8") as f:
                    prompt_text = f.read().strip()

                prompt_speech_16k = load_wav(os.path.join(target_vocal_dir, f"{tone}.wav"), 16000)
                for i, j in enumerate(
                    cosyvoice.inference_zero_shot(text, prompt_text, prompt_speech_16k, stream=False)
                ):
                    torchaudio.save(
                        os.path.join(seg_dir, f"{cnt}.wav"),
                        j["tts_speech"],
                        cosyvoice.sample_rate,
                    )

                if "reaction" in result:
                    reaction = result["reaction"].lower()
                    reaction_path = os.path.join(reaction_dir, f"{reaction}.wav")

                    try:
                        original_audio = AudioSegment.from_file(os.path.join(seg_dir, f"{cnt}.wav"))
                        reaction_audio = AudioSegment.from_file(reaction_path)

                        combined_audio = original_audio + reaction_audio

                        combined_audio.export(os.path.join(seg_dir, f"{cnt}.wav"), format="wav")
                        print(f"Successfully combined reaction audio for line {cnt}.")
                    except Exception as e:
                        print(f"Error combining reaction audio for line {cnt}: {str(e)}")

                results.append(result)
                cnt += 1
            except Exception as e:
                print(f"Error processing line: {line}. Error: {str(e)}")
                continue

        synth_audio_path = self.merge_audio_files(seg_dir, cnt)
        print(f"Final combined audio saved at: {synth_audio_path}")
        os.chdir(current_dir)
        metadata_path = os.path.join(os.path.dirname(target_vocal_dir), "stand-up.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return {
            "audio_path": synth_audio_path,
            "seg_dir": seg_dir,
            "metadata_path": results,
        }
