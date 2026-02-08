# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_conversion.py
import json
import os

from environment.agents.base import BaseTool
from environment.config.llm import deepseek
from pydantic import BaseModel, Field


class VideoConversion(BaseTool):
    """
    Agent that converts audio content with JSON timestamps into visual scene descriptions for video generation.
    It often needs to be paired with SVCConversion, StandUpConversion, or CrossTalkConversion.
    """

    def __init__(self):
        super().__init__()
        # Get the current directory
        current_dir = os.getcwd()
        self.video_edit_dir = os.path.join(current_dir, "dataset/video_edit")
        self.scene_output_dir = os.path.join(self.video_edit_dir, "scene_output")
        self.audio_analysis_dir = os.path.join(self.video_edit_dir, "audio_analysis")

        # Create necessary directories
        os.makedirs(self.scene_output_dir, exist_ok=True)
        os.makedirs(self.audio_analysis_dir, exist_ok=True)

    class InputSchema(BaseTool.BaseInputSchema):
        timestamp_path: str = Field(
            ...,
            description="File path storing video segment timestamps for seamless video switching during editing",
        )

    class OutputSchema(BaseModel):
        video_scene_path: str = Field(
            ...,
            description="File path storing scene semantics for video storyboard sound synthesis.",
        )

    def _process_with_llm(self, content):
        """Send content to LLM for scene translation using the exact specified prompt"""
        system_prompt = """
        You are a visual scene descriptor. Follow these exact requirements:

        Key requirements:
        - Keep the number of "/////" mark unchanged.
        - You CAN ONLY deduce by English visual-scene description.
        - Deduce visual-scene description in English for each sections.
        - Keep the same number of sentence separators and spacing.
        - Each scene sections' description don't exceed 1 sentences.
        - Don't directly translate each sentences.
        - If the sections contains character name, deduce that character's appearance.
        - Whenever a character is mentioned by name within the sections, the scene description must describe the character's appearance (eg. [Robert Downey Jr.] >>> Robert Downey Jr. a white male with deep brown eyes and a signature goatee.)
        """

        user_prompt = f"""
        Content to process:
        {content}

        Example Input:
        /////\n[Emily] and [Jackson] stood together, the ocean breeze ruffling their hair, both soaking up the moment, surrounded by the vastness of the ocean, which reflected their budding love.\n\n/////\nThe leader increased Xiao Wang's business freedom by changing the company's management rules.

        Example Output:
        /////\nA Red hair girl Emily and brown hair boy Jackson standing together on the sunset seaside with hair blown by the wind\n\n/////\nwhite t-shirt young employees within office environment

        Now process this content following all the rules above:
        {content}
        """

        response = deepseek(system=system_prompt, user=user_prompt)

        if hasattr(response, "choices") and len(response.choices) > 0:
            if hasattr(response.choices[0], "message") and hasattr(response.choices[0].message, "content"):
                return response.choices[0].message.content

        # Fallback if response structure is different
        return str(response)

    def execute(self, **kwargs):
        """Execute the scene description generation process"""
        # Validate input parameters
        params = self.InputSchema(**kwargs)

        # Set default paths if not provided
        timestamps_file = params.timestamp_path or os.path.join(self.audio_analysis_dir, "cut_points.json")
        output_file = os.path.join(self.scene_output_dir, "video_scene.json")
        video_scene_path = output_file

        print("\n=== GENERATING SCENE DESCRIPTIONS ===")

        # Check if timestamps file exists
        if not os.path.exists(timestamps_file):
            return {
                "scene_file": "",
                "segment_count": 0,
                "status": "error",
                "error": f"Timestamps file not found: {timestamps_file}",
            }

        # Load the JSON data from the timestamps file
        print(f"Reading timestamps from: {timestamps_file}")
        with open(timestamps_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract content from each chunk
        contents = []
        try:
            contents = [chunk["content"] for chunk in data["sentence_data"]["chunks"]]
            print(f"Found {len(contents)} content segments")
        except KeyError as e:
            return {
                "status": "error",
                "error": f"Invalid timestamps file format: {str(e)}",
            }

        if not contents:
            return {
                "status": "error",
                "error": "No content segments found in timestamps file",
            }

        # Format content with separators
        formatted_content = "/////\n" + "\n\n/////\n".join(contents)

        translated_content = self._process_with_llm(formatted_content)

        # Prepare output structure
        output_data = {"segment_scene": translated_content}

        # Optionally preserve the original content
        output_data["content_created"] = formatted_content

        # Create directory if needed
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save output to file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)

        print(f"Successfully processed and saved scene descriptions to {output_file}")

        return {"video_scene_path": video_scene_path}
