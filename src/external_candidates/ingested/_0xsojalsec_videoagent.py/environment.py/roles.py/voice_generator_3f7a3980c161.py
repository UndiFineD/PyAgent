# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\voice_generator.py
import json
import os
import re
import traceback

import torch
import torchaudio
from environment.agents.base import BaseTool
from pydantic import BaseModel, Field


class VoiceGenerator(BaseTool):
    """
    Agent processes scene content, generates speech audio, and provides timestamp information for video editing.
    The VoiceGenerator focuses on generating speech based on scene content (e.g., descriptions, narration, or supplemental audio) rather than modifying the original video's dialogue and synthesizing replacements for a revised script.
    It is commonly used for voice synthesis in Commentary, News, and Rhythm-based content.
    """

    def __init__(self):
        super().__init__()
        # Navigate to the project root directory (three levels up from current file)
        self.project_root = os.getcwd()

        # Path to CosyVoice in the tools directory
        cosyvoice_dir = os.path.join(self.project_root, "tools", "CosyVoice")
        matcha_dir = os.path.join(cosyvoice_dir, "third_party", "Matcha-TTS")

        # Set up paths
        self.model_path = os.path.join(
            self.project_root,
            "tools",
            "CosyVoice",
            "pretrained_models",
            "CosyVoice2-0.5B",
        )
        self.video_edit_dir = os.path.join(self.project_root, "dataset", "video_edit")
        self.scene_output_dir = os.path.join(self.video_edit_dir, "scene_output")
        self.audio_analysis_dir = os.path.join(self.video_edit_dir, "audio_analysis")
        self.storyboard_file = os.path.join(self.scene_output_dir, "video_scene.json")
        self.audio_path = os.path.join(self.audio_analysis_dir, "gen_audio.wav")

        os.makedirs(self.video_edit_dir, exist_ok=True)
        os.makedirs(self.scene_output_dir, exist_ok=True)
        os.makedirs(self.audio_analysis_dir, exist_ok=True)

        # CosyVoice and prompt will be initialized later
        self.CosyVoice2 = None
        self.load_wav = None
        self.cosyvoice = None
        self.prompt_speech_16k = None

    class InputSchema(BaseTool.BaseInputSchema):
        video_scene_path: str = Field(
            ..., description="Path to a custom scene JSON file"
        )
        target_vocal_path: str = Field(
            ..., description="Path to the target timbre for voice generation"
        )

    class OutputSchema(BaseModel):
        audio_path: str = Field(..., description="Path to the synthesized audio")
        timestamp_path: str = Field(..., description="Path to video frame timestamp")

    def _import_dependencies(self):
        """Import CosyVoice modules"""
        if self.CosyVoice2 is None:
            try:
                from cosyvoice.cli.cosyvoice import CosyVoice2
                from cosyvoice.utils.file_utils import load_wav

                self.CosyVoice2 = CosyVoice2
                self.load_wav = load_wav
                return True
            except ImportError as e:
                print(f"Error importing CosyVoice modules: {e}")
                return False
        return True

    def _process_with_timestamps(self, json_file_path):
        """Process JSON file and extract segments with proper support for Chinese content"""
        # Read the JSON file
        with open(
            json_file_path, "r", encoding="utf-8"
        ) as file:  # Ensure UTF-8 encoding
            json_data = json.load(file)

        # Get the raw content - check both possible field names
        raw_content = None
        if "content_created" in json_data:
            raw_content = json_data["content_created"]
            print("Using 'content_created' field from JSON")
        else:
            print("Error: 'content_created' field not found in JSON file")
            return []

        # Normalize line endings
        raw_content = raw_content.replace("\r\n", "\n")

        # Check for the exact delimiter pattern from your example
        if "/////\n" in raw_content:
            segments = raw_content.split("/////\n")
            print("Using exact '/////\n' delimiter pattern")
        else:
            # Fallback to more generic regex pattern
            segments = re.split(r"/+\s*\n", raw_content)
            print("Using regex pattern for delimiter detection")

        # Filter out empty segments and strip whitespace
        segments = [seg.strip() for seg in segments if seg.strip()]

        # Create a list to store both full content and individual segments
        segment_list = []
        for i, segment in enumerate(segments):
            segment_list.append({"segment_id": i + 1, "content": segment})

        # Create a new object with the full content and segments
        clean_json = {
            "user_idea": json_data.get("user_idea", ""),
            "segments": segment_list,
        }

        # Save to a new file with UTF-8 encoding
        output_path = json_file_path.replace(".json", "_clean.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                clean_json, f, indent=2, ensure_ascii=False
            )  # ensure_ascii=False to preserve Chinese characters

        print(f"Original content had {len(segments)} segments separated by delimiters")
        print(f"Clean content saved to {output_path}")

        return segment_list

    def _split_into_sentences(self, text, max_length=200):
        """Split text into manageable chunks for TTS processing with Chinese support"""
        # Chinese sentences typically use different punctuation
        for punct in ["。", "！", "？", "；", ". ", "! ", "? ", "; "]:
            text = text.replace(punct, punct + "|")

        sentences = text.split("|")
        sentences = [s.strip() for s in sentences if s.strip()]

        # Further split long sentences
        result = []
        for sentence in sentences:
            if len(sentence) <= max_length:
                result.append(sentence)
            else:
                # Split by commas and Chinese commas if sentence is too long
                comma_parts = sentence.replace("，", ",").split(",")
                current_part = ""

                for part in comma_parts:
                    if len(current_part) + len(part) <= max_length:
                        if current_part:
                            current_part += "," + part
                        else:
                            current_part = part
                    else:
                        if current_part:
                            result.append(current_part)
                        current_part = part

                if current_part:
                    result.append(current_part)

        return result

    def _generate_audio_for_segments(self, segments, output_dir, max_sentence_length):
        """Generate audio for each segment and track timestamps with Chinese support"""
        if output_dir is None:
            output_dir = self.audio_analysis_dir

        # Make sure output_dir exists
        os.makedirs(output_dir, exist_ok=True)

        timestamp_data = {"sentence_data": {"count": len(segments), "chunks": []}}

        current_time = 0  # Running timestamp in seconds
        all_segment_waveforms = []
        all_files_to_delete = []  # Track all files for cleanup

        # Process each segment
        for segment in segments:
            segment_id = segment["segment_id"]
            segment_text = segment["content"]
            segment_output_file = os.path.join(output_dir, f"segment_{segment_id}.wav")
            all_files_to_delete.append(segment_output_file)  # Add to list for cleanup

            print(f"\nProcessing Segment {segment_id}:")
            # For Chinese, we display fewer characters in preview
            text_preview = (
                segment_text[:50] + "..." if len(segment_text) > 50 else segment_text
            )
            print(f"Text preview: {text_preview}")

            # Skip any segments that still contain the separator pattern
            if "//////" in segment_text:
                print(f"Skipping segment {segment_id} as it appears to be a separator")
                continue

            # Split segment into sentences/chunks for processing
            sentences = self._split_into_sentences(
                segment_text, max_length=max_sentence_length
            )
            print(f"Split into {len(sentences)} chunks for processing")

            # Skip if no valid sentences
            if not sentences:
                print(f"No valid sentences found in segment {segment_id}, skipping")
                continue

            # Track segment start time
            segment_start_time = current_time
            segment_waveform = None

            # Process each sentence individually
            for i, sentence in enumerate(sentences):
                try:
                    # For Chinese, we display fewer characters in preview
                    sentence_preview = (
                        sentence[:30] + "..." if len(sentence) > 30 else sentence
                    )
                    print(
                        f"  Processing chunk {i+1}/{len(sentences)}: '{sentence_preview}'"
                    )

                    # Create a generator for just this one sentence
                    def single_sentence_generator():
                        yield sentence

                    chunk_waveform = None

                    # Process this single sentence
                    for audio_data in self.cosyvoice.inference_zero_shot(
                        single_sentence_generator(),
                        "hello everyone, I'm your assistant OpenAI Chat GPT.",
                        self.prompt_speech_16k,
                        stream=False,
                    ):

                        # Store this chunk's waveform
                        chunk_waveform = audio_data["tts_speech"]

                    # Add to segment waveform
                    if chunk_waveform is not None:
                        if segment_waveform is None:
                            segment_waveform = chunk_waveform
                        else:
                            segment_waveform = torch.cat(
                                [segment_waveform, chunk_waveform], dim=1
                            )
                        print(f"    Successfully processed chunk {i+1}")
                    else:
                        print(f"    Warning: No audio generated for chunk {i+1}")

                except Exception as e:
                    print(f"  Error processing chunk {i+1}: {str(e)}")
                    print("  Continuing to next chunk...")

            # Save the complete segment audio file
            if segment_waveform is not None:
                torchaudio.save(
                    segment_output_file, segment_waveform, self.cosyvoice.sample_rate
                )

                # Calculate segment duration
                segment_duration = len(segment_waveform[0]) / self.cosyvoice.sample_rate

                # Update the current time
                current_time += segment_duration

                # Add to timestamp data
                timestamp_data["sentence_data"]["chunks"].append(
                    {
                        "id": segment_id,
                        "timestamp": round(current_time, 3),
                        "content": segment_text,
                    }
                )

                # Store the waveform for later concatenation
                all_segment_waveforms.append(segment_waveform)

                print(
                    f"Successfully processed segment {segment_id} (duration: {segment_duration:.2f}s)"
                )
            else:
                print(f"Warning: No audio generated for segment {segment_id}")

        # Cleanup any chunk files that may have been created previously
        chunk_files = [
            f
            for f in os.listdir(output_dir)
            if f.startswith("segment_") and "_chunk_" in f
        ]
        for chunk_file in chunk_files:
            all_files_to_delete.append(os.path.join(output_dir, chunk_file))

        # Return timestamp data, all waveforms, and files for cleanup
        return (
            timestamp_data,
            all_segment_waveforms,
            self.cosyvoice.sample_rate,
            all_files_to_delete,
            current_time,
        )

    def _combine_audio_files(
        self,
        all_segment_waveforms,
        sample_rate,
        timestamp_data,
        output_file,
        segment_files,
        keep_segment_files,
    ):
        """
        Combine all segment waveforms into one and save as WAV file
        Also save timestamp data to JSON and delete all intermediate files
        """
        if not all_segment_waveforms:
            print("No audio segments to combine")
            return None, None

        # Combine all waveforms
        combined_waveform = all_segment_waveforms[0]
        for waveform in all_segment_waveforms[1:]:
            combined_waveform = torch.cat([combined_waveform, waveform], dim=1)

        # Export combined audio as WAV
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        # Save the combined waveform
        torchaudio.save(output_file, combined_waveform, sample_rate)
        print(f"Combined audio saved to: {output_file}")

        # Save timestamp JSON with UTF-8 encoding to preserve Chinese characters
        timestamp_json_file = os.path.join(output_dir, "cut_points.json")
        with open(timestamp_json_file, "w", encoding="utf-8") as f:
            json.dump(
                timestamp_data, f, indent=2, ensure_ascii=False
            )  # ensure_ascii=False preserves Chinese characters
        print(f"Timestamp data saved to: {timestamp_json_file}")

        # Clean up all files - both segment files and chunk files
        if not keep_segment_files and segment_files:
            print("Cleaning up temporary files...")
            deleted_count = 0
            for file_path in segment_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                except Exception as e:
                    print(f"Warning: Could not remove {file_path}: {str(e)}")
            print(f"Removed {deleted_count} temporary files")

        return output_file, timestamp_json_file

    def _initialize_model(self, prompt_speech_path):
        """Initialize the CosyVoice2 model"""
        # Import dependencies if needed
        if not self._import_dependencies():
            return False

        print(f"Ensuring all necessary directories exist in: {self.video_edit_dir}")

        # Initialize CosyVoice2
        print("Loading CosyVoice2 model...")
        self.cosyvoice = self.CosyVoice2(
            self.model_path, load_jit=False, load_trt=False, fp16=False
        )

        # Check if prompt file exists, warn if not
        if not os.path.exists(prompt_speech_path):
            print(f"Error: Prompt speech file not found at {prompt_speech_path}")
            return False

        # Load the prompt for zero-shot learning
        print("Loading prompt speech file...")
        self.prompt_speech_16k = self.load_wav(prompt_speech_path, 16000)
        return True

    def execute(self, **kwargs):
        """Execute the voice generation process"""
        # Validate input parameters
        params = self.InputSchema(**kwargs)

        # Set default paths if not provided
        scene_file = self.storyboard_file
        prompt_speech_file = params.target_vocal_path
        output_file = self.audio_path

        try:
            print("\n=== GENERATING VOICE ===")

            # Initialize the model
            if not self._initialize_model(prompt_speech_file):
                return

            # Check if scene file exists
            if not os.path.exists(scene_file):
                return
            # Process content from the scene file
            print(f"Processing content from: {scene_file}")
            segments = self._process_with_timestamps(scene_file)

            if not segments:
                return
            print(f"Found {len(segments)} segments to process")

            # Generate audio with timestamp tracking
            (
                timestamp_data,
                all_segment_waveforms,
                sample_rate,
                files_to_delete,
                total_duration,
            ) = self._generate_audio_for_segments(
                segments, output_dir=self.audio_analysis_dir, max_sentence_length=200
            )

            if not all_segment_waveforms:
                return

            # Combine all segments, save timestamp JSON, and delete all intermediate files
            final_audio_path, timestamp_json_path = self._combine_audio_files(
                all_segment_waveforms,
                sample_rate,
                timestamp_data,
                output_file=output_file,
                segment_files=files_to_delete,
                keep_segment_files=False,
            )

            print(f"Audio successfully generated and saved to: {output_file}")
            return {
                "audio_path": final_audio_path,
                "timestamp_path": timestamp_json_path,
            }

        except Exception as e:
            print(f"An error occurred in the voice generation process: {str(e)}")
            traceback.print_exc()
            return
