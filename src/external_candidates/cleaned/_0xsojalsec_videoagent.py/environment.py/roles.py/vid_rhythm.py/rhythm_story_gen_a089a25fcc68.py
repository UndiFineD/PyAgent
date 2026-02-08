# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_rhythm\rhythm_story_gen.py
import json
import math
import os
import time
from typing import List

import tenacity
from environment.agents.base import BaseTool
from environment.config.llm import gpt
from pydantic import BaseModel, Field


class RhythmContentGenerator(BaseTool):
    """
    Application scenario: Rhythm-cut music video creating
    Agent that extracts video segment content, creates scene-focused narrative summaries, and generates rhythm-aware storyboards incorporating user ideas.
    """

    def __init__(self):
        super().__init__()
        self.max_tokens = 16384

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(..., description="User requirements for the storyboard")
        rhythm_analysis_dir: str = Field(..., description="Directory containing audio rhythm analysis results")

    class OutputSchema(BaseModel):
        video_scene_path: str = Field(
            ...,
            description="File path storing scene semantics for video storyboard sound synthesis.",
        )
        timestamp_path: str = Field(
            ...,
            description="File path storing video segment timestamps for seamless video switching during editing",
        )

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
        stop=tenacity.stop_after_attempt(5),
        before_sleep=lambda retry_state: print(
            f"API call failed. Retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number})"
        ),
    )
    def _call_llm_api(self, prompt=None, system=None, max_tokens=None, temperature=0.7):
        """Call LLM API with retry logic using tenacity."""
        if system:
            response = gpt(system=system, user=prompt)
        else:
            response = gpt(user=prompt)
        return response

    def _extract_video_content(self, video_segments_path, summary_output_path, chunks=4):
        """Process the video segments file in multiple chunks and generate narrative-focused summaries."""
        # Load data
        print(f"Loading data from {video_segments_path}")
        with open(video_segments_path, "r", encoding="utf-8") as file:
            segments_data = json.load(file)

        # Extract all content
        all_contents = []
        for video_key, segments in segments_data.items():
            for segment_id, segment_data in segments.items():
                if "content" in segment_data:
                    all_contents.append(segment_data["content"])

        # Split into multiple chunks
        chunk_size = math.ceil(len(all_contents) / chunks)
        content_chunks = []

        for i in range(0, len(all_contents), chunk_size):
            chunk = all_contents[i : i + chunk_size]
            content_chunks.append("\n\n".join(chunk))

        print(f"Split content into {len(content_chunks)} parts with approximately {chunk_size} segments each")

        # Process each chunk
        chunk_summaries = []
        for i, chunk_content in enumerate(content_chunks):
            print(f"Creating narrative summary for chunk {i + 1}/{len(content_chunks)}...")
            chunk_summary = self._get_chunk_summary(chunk_content, i + 1, len(content_chunks))
            chunk_summaries.append(chunk_summary)

            # Add a small delay between API calls to avoid rate limiting
            if i < len(content_chunks) - 1:
                time.sleep(1)

        # First combine pairs of summaries to reduce the number of chunks
        if len(chunk_summaries) > 2:
            print("Combining chunk summaries into intermediate summaries...")
            intermediate_summaries = []

            for i in range(0, len(chunk_summaries), 2):
                if i + 1 < len(chunk_summaries):
                    # Combine pair of summaries
                    combined = self._combine_pair(chunk_summaries[i], chunk_summaries[i + 1], i // 2 + 1)
                    intermediate_summaries.append(combined)
                else:
                    # Handle odd number of summaries
                    intermediate_summaries.append(chunk_summaries[i])

                # Add delay between API calls
                if i + 2 < len(chunk_summaries):
                    time.sleep(1)

            # Replace chunk_summaries with intermediate_summaries for final combination
            chunk_summaries = intermediate_summaries

        # Final combination of all summaries
        print("Creating final cohesive narrative...")
        final_summary = self._combine_all_narratives(chunk_summaries)

        # Save detailed information to file
        output_data = {
            "video_summary": final_summary,
            "chunk_summaries": chunk_summaries,
        }

        with open(summary_output_path, "w", encoding="utf-8") as file:
            json.dump(output_data, file, indent=2, ensure_ascii=False)

        print(f"Narrative summary saved to {summary_output_path}")

        return output_data

    def _get_chunk_summary(self, content: str, chunk_number: int, total_chunks: int) -> str:
        """Create a scene-focused narrative summary of a content chunk."""
        prompt = f"""You are analyzing part {chunk_number} of {total_chunks} from a video or film. Create a brief narrative summary that focuses on the storytelling elements and scene details. 

        For each important scene or sequence:
        - Describe the setting, atmosphere, and visual elements
        - Identify key characters and their actions or interactions
        - Capture any important dialogue or narrative developments
        - Note any significant emotional moments

        Your summary should flow like a cohesive story, following the narrative arc present in this part of the video. Don't just list scenes - create a flowing narrative that captures the storytelling.

        Here is part {chunk_number} of {total_chunks} of the video content:

        {content}
        """

        try:
            response = self._call_llm_api(prompt=prompt)
            return response.choices[0].message.content
        except Exception as e:
            print(f"All retry attempts failed for chunk {chunk_number}: {str(e)}")
            return f"Error generating summary for part {chunk_number}: {str(e)}"

    def _combine_pair(self, first_summary: str, second_summary: str, pair_number: int) -> str:
        """Combine a pair of consecutive narrative summaries."""
        prompt = f"""You have two consecutive narrative summaries from parts of the same video or film.

        First summary:
        {first_summary}

        Second summary:
        {second_summary}

        Create a single cohesive narrative that combines these two parts. The combined narrative should:
        - Flow naturally as one story section
        - Connect character developments and plot points between the two parts
        - Maintain important scenes and storytelling elements
        - Be concise but comprehensive
        
        This combined narrative will later be merged with other section summaries.
        """

        try:
            response = self._call_llm_api(prompt=prompt, temperature=0.3)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error combining pair {pair_number}: {e}")
            # Fallback to simple concatenation
            return f"Part {pair_number}A: {first_summary}\n\nPart {pair_number}B: {second_summary}"

    def _combine_all_narratives(self, summaries: List[str]) -> str:
        """Combine all narrative summaries into one cohesive story."""
        summaries_text = "\n\n---\n\n".join([f"Part {i + 1}:\n{summary}" for i, summary in enumerate(summaries)])

        prompt = f"""You have multiple narrative summaries describing different parts of the same video or film.

        {summaries_text}

        Create a single cohesive narrative that tells the complete story of the video from beginning to end. The final narrative should:
        - Be highly summarized but complete
        - Flow naturally as one complete story
        - Maintain the important scenes and storytelling elements from all parts
        - Preserve the narrative arc across the entire video
        - Connect character developments and plot points across all parts
        - Read as if it was written as a single narrative summary

        Your combined narrative should capture the full storytelling experience of the video from start to finish in a concise and engaging way.
        """

        try:
            response = self._call_llm_api(prompt=prompt, temperature=0.4)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error creating final combined narrative: {e}")
            # Fallback to simple concatenation
            return "Complete Video Narrative:\n\n" + "\n\n".join(
                [f"Part {i + 1}: {summary}" for i, summary in enumerate(summaries)]
            )

    def _create_storyboard(self, user_idea, audio_json_path, rhythm_plot_path, video_summary=None):
        """Generate a rhythm-aware storyboard incorporating user ideas and optional video content."""

        # Default to 10 sections if JSON file doesn't exist
        sections_num = 10
        try:
            if os.path.exists(audio_json_path):
                with open(audio_json_path, "r", encoding="utf-8") as file:
                    sectionsdata = json.load(file)
                    sections_num = sectionsdata["beat_data"]["count"]
                    print(f"Found {sections_num} rhythm sections in audio analysis")
            else:
                print(f"Audio JSON file not found at {audio_json_path}, using default of {sections_num} sections")
        except Exception as e:
            print(f"Error reading audio JSON file: {e}. Using default of {sections_num} sections")

        # Check if rhythm plot exists
        rhythm_reference = ""
        if os.path.exists(rhythm_plot_path):
            rhythm_reference = f"""
            Background Music Visualization with Rhythm Points for Reference:
            [View the rhythm points visualization plot at {rhythm_plot_path}]
            - The plot shows the musical intensity and rhythm patterns over time
            - Peaks represent high-energy moments
            - Valleys indicate calmer, quieter segments
            - Use this visualization to guide scene pacing and emotional intensity
            """
        else:
            rhythm_reference = "Note: No rhythm visualization is available. Create scenes with your own rhythm pacing."

        # Add video summary reference if provided
        video_reference = ""
        if video_summary:
            video_reference = f"""
            Supplementary Reference Material (If needed):
            {video_summary}
            """

        system_prompt = "You are a creative director specializing in rhythm-based visual storyboard creation, strictly follow user's requirements."

        user_prompt = f"""
        Create a rhythm-synchronized storyboard that aligns with user requirements and musical elements.

        {rhythm_reference}

        Total Scenes Required: {sections_num}
        ###################################

        User creative requests (high priority):
        "{user_idea}"
        ###################################

        Storyboard Creation Guidelines:

        1. Scene Structure:
        - Begin each scene with /////
        - Number scenes from 1 to {sections_num}
        - Align scene transitions and rhythm
        - Balance scene energy with musical flow

        2. Visual Requirements:
        - Provide detailed character appearances in every scene (e.g., "Spider-Gwen in white and pink suit with a hood and ballet shoes on a train")
        - Include specific visual elements
        - Capture the mood through visual atmosphere
        - No dialogue design required
        - Include rich motion and visual descriptions

        3. Rhythm Integration:
        - Match scene intensity with visualization pattern
        - Use peaks for impactful moments

        4. Content Rules:
        - Can not exceed two sentences per scene
        - Focus on visual and emotional elements
        - Keep descriptions clear, concise and short
        - Maintain narrative flow between scenes

        Format Output Example:

        /////\n[Scene description]\n\n/////\n[Scene description]

        {video_reference}
        """

        try:
            response = self._call_llm_api(system=system_prompt, prompt=user_prompt, temperature=0.7)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error creating storyboard: {str(e)}"

    def execute(self, **kwargs):
        """Run the complete pipeline to extract video content and create a storyboard."""
        # Validate input parameters
        params = self.InputSchema(**kwargs)
        use_video_content = False
        user_idea = params.reqs

        # Define base directory paths
        current_dir = os.getcwd()
        video_edit_dir = os.path.join(current_dir, "dataset/video_edit")
        scene_output_dir = os.path.join(video_edit_dir, "scene_output")
        # Create directories if they don't exist
        os.makedirs(scene_output_dir, exist_ok=True)
        rhythm_analysis_dir = params.rhythm_analysis_dir
        workdir = os.path.join(video_edit_dir, "videosource-workdir")

        # Updated file paths
        video_segments_path = os.path.join(workdir, "kv_store_video_segments.json")
        video_summary_path = os.path.join(scene_output_dir, "video_summary.json")
        video_scene_path = os.path.join(scene_output_dir, "video_scene.json")
        timestamp_path = os.path.join(rhythm_analysis_dir, "cut_points.json")
        rhythm_detection_path = os.path.join(rhythm_analysis_dir, "rhythm_detection.png")

        # Variables to hold our data
        video_summary = None

        # Check if use_video_content is a string (from config) and convert to boolean
        if isinstance(use_video_content, str):
            use_video_content = use_video_content == "1"

        # Process video content if requested
        if use_video_content and os.path.exists(video_segments_path):
            print("\n=== STAGE 1: EXTRACTING AND SUMMARIZING VIDEO CONTENT ===")
            summary_results = self._extract_video_content(
                video_segments_path=video_segments_path,
                summary_output_path=video_summary_path,
            )
            video_summary = summary_results.get("video_summary", "")
        else:
            if use_video_content:
                print(f"Video segments file not found at {video_segments_path}")
            print("Creating storyboard based on your idea only.")

        # If user_idea is not provided (should never happen with the validation)
        if user_idea is None or user_idea == "":
            user_idea = "A creative music video with visual effects"
            print(f"Using default idea: {user_idea}")
        else:
            print(f"Using provided idea: {user_idea}")

        # Check if audio analysis files exist
        if not os.path.exists(timestamp_path):
            print(f"Warning: Audio analysis file not found at {timestamp_path}")
            print("The storyboard will be created without rhythm information.")
            print("Run music analysis first to include rhythm data in your storyboard.")

        # Create storyboard with rhythm plot reference
        storyboard = self._create_storyboard(
            user_idea=user_idea,
            audio_json_path=timestamp_path,
            rhythm_plot_path=rhythm_detection_path,
            video_summary=video_summary,
        )

        # Save storyboard output
        storyboard_output = {
            "user_idea": user_idea,
            "video_summary": video_summary,
            "segment_scene": storyboard,
        }

        with open(video_scene_path, "w", encoding="utf-8") as f:
            json.dump(storyboard_output, f, indent=2, ensure_ascii=False)

        print("\nStoryboard saved to", video_scene_path)
        print("\nStoryboard Preview:")
        print(storyboard[:1000] + "..." if len(storyboard) > 1000 else storyboard)

        return {"video_scene_path": video_scene_path, "timestamp_path": timestamp_path}
