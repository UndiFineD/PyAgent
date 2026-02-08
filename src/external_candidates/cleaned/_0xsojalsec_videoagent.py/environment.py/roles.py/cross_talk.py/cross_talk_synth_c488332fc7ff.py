# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\cross_talk\cross_talk_synth.py
import json
import os

import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
from environment.agents.base import BaseTool
from environment.config.llm import deepseek
from pydantic import BaseModel, Field
from pydub import AudioSegment


class CrossTalkSynth(BaseTool):
    """
    Application scenario: Cross Talk Creating
    Segment-by-segment cross talk audio synthesis with final merge
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        script: str = Field(..., description="String of segmented cross talk script")
        dou_gen_dir: str = Field(..., description="The 逗哏 tone directory for cross talk synthesis.")
        peng_gen_dir: str = Field(..., description="The 捧哏 tone directory for cross talk synthesis.")

    class OutputSchema(BaseModel):
        audio_path: str = Field(..., description="File path to the synthesized cross talk audio")
        seg_dir: str = Field(..., description="Directory containing all segmented cross talk audio files")
        metadata_path: str = Field(..., description="File path to the metadata of the cross talk script")

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
        output_file_path = os.path.join(parent_dir, "final", "cross_talk.wav")
        merged_audio.export(output_file_path, format="wav")
        abs_output_file_path = os.path.abspath(output_file_path)
        print(f"Combined audio saved to {abs_output_file_path}")

        return os.path.abspath(output_file_path)

    def execute(self, **kwargs):
        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        script = params.script
        dou_gen_dir = os.path.abspath(params.dou_gen_dir)
        peng_gen_dir = os.path.abspath(params.peng_gen_dir)
        data_dir = os.path.dirname(peng_gen_dir)
        dou_gen_name = os.path.basename(dou_gen_dir)
        peng_gen_name = os.path.basename(peng_gen_dir)

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

        results = []
        text_list = []
        cnt = 0
        first_line = True
        seg_dir = os.path.join(os.path.dirname(dou_gen_dir), "seg")
        os.makedirs(seg_dir, exist_ok=True)

        for line in script.split("\n"):
            if not line.strip():
                continue

            if first_line:
                first_line = False
                continue

            user_prompt = f"""
            Analyze the following crosstalk dialogue line for performer role, tone, text content and audience reaction:
            {line}

            Output JSON format with STRICT rules:
            1. "role" field must be either {dou_gen_name} or {peng_gen_name}
            2. "tone" field must be "Natural", "Emphatic" or "Confused"
            3. "text" field contains the dialogue content
            4. Add "reaction" field ONLY if [Laughter] or [Cheers] exists (value must be "Laughter" or "Cheers")
            5. No extra characters before/after JSON

            Example 1:
            {{
                "role": "{dou_gen_name}",
                "tone": "Natural",
                "text": "...",
                "reaction": "Cheers"
            }}

            Example 2:
            {{
                "role": "{peng_gen_name}",
                "tone": "Emphatic",
                "text": "..."
            }}

            Strictly ensure:
            - Valid JSON syntax
            - Double quotes for strings
            - Do not add any characters before or after the JSON structure

            Output ONLY the JSON object!
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
                role = result["role"]
                tone = result["tone"].strip().lower()
                text = result["text"].strip()
                text_list.append(text)

                with open(os.path.join(data_dir, role, f"{tone}.lab"), "r", encoding="utf-8") as f:
                    prompt_text = f.read().strip()

                prompt_speech_16k = load_wav(os.path.join(data_dir, role, f"{tone}.wav"), 16000)
                for i, j in enumerate(
                    cosyvoice.inference_zero_shot(text, prompt_text, prompt_speech_16k, stream=False)
                ):
                    torchaudio.save(
                        os.path.join(seg_dir, f"{cnt}.wav"),
                        j["tts_speech"],
                        cosyvoice.sample_rate,
                    )

                results.append(result)
                cnt += 1
            except Exception as e:
                print(f"Error processing line: {line}. Error: {str(e)}")
                continue

        synth_audio_path = self.merge_audio_files(seg_dir, cnt)
        print(f"Final combined audio saved at: {synth_audio_path}")
        os.chdir(current_dir)
        metadata_path = os.path.join(data_dir, "cross-talk.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return {
            "audio_path": synth_audio_path,
            "seg_dir": seg_dir,
            "metadata_path": metadata_path,
        }
