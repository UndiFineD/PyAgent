# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_searcher.py
import json
import logging
import multiprocessing
import os
import sys
import warnings

from environment.agents.base import BaseTool
from pydantic import BaseModel, Field


class VideoSearcher(BaseTool):
    """
    Agent that retrieves matching video clips from video_dir based on multiple semantic subquries: VideoPreloader must be called and upstream agents need to provide video scene file (unless explicitly specified that user provides video scene file, which not timestamp file.)
    Note: VideoPreloader, VideoSearcher, and VideoEditor need to be called together.
    """

    def __init__(self):
        super().__init__()
        # Configure logging and warnings
        warnings.filterwarnings("ignore")
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        # Set up paths
        self._setup_paths()

        # VideoRAG objects will be initialized when needed
        self.VideoRAG = None
        self.QueryParam = None

    class InputSchema(BaseTool.BaseInputSchema):
        video_scene_path: str = Field(
            ...,
            description="File path storing scene semantics for video storyboard sound synthesis.",
        )

    class OutputSchema(BaseModel):
        status: str = Field(..., description="Execution status (success/error)")

    def _setup_paths(self):
        """Set up necessary paths and directories"""
        current_dir = os.getcwd()
        # Define paths
        self.dataset_dir = os.path.join(current_dir, "dataset")
        self.video_edit_dir = os.path.join(self.dataset_dir, "video_edit")
        self.scene_output_dir = os.path.join(self.video_edit_dir, "scene_output")
        self.scene_output_path = os.path.join(self.scene_output_dir, "video_scene.json")
        self.working_dir = os.path.join(self.video_edit_dir, "videosource-workdir")

        # Create directories if they don't exist
        os.makedirs(self.video_edit_dir, exist_ok=True)
        os.makedirs(self.working_dir, exist_ok=True)
        os.makedirs(self.scene_output_dir, exist_ok=True)

        # Add tools directory to path
        tools_dir = os.path.join(current_dir, "tools")
        if tools_dir not in sys.path:
            sys.path.append(tools_dir)

    def _load_videorag(self):
        """Import VideoRAG dependencies that require specific path setup"""
        if self.VideoRAG is None:
            try:
                from videorag.videoragcontent import QueryParam, VideoRAG

                self.VideoRAG = VideoRAG
                self.QueryParam = QueryParam
                self.logger.info("VideoRAG modules loaded successfully")
                return True
            except ImportError as e:
                self.logger.error(f"Failed to import VideoRAG: {e}")
                return False
        return True

    def _process_scene(self, scene_file: str, working_dir: str, use_references: bool):
        """
        Process a scene from JSON and use VideoRAG to search for matching content

        Args:
            scene_file: Path to the scene JSON file
            working_dir: Working directory for VideoRAG
            use_references: Whether to include references in the response

        Returns:
            Dictionary with search results and status
        """
        try:
            # Make sure VideoRAG is loaded
            if not self._load_videorag():
                return
            # Load the scene file
            with open(scene_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Extract the content
            segment_scene = data.get("segment_scene", "")

            if not segment_scene:
                self.logger.warning("Empty segment_scene found in the JSON file")
                return

            # Use the content as query
            query = segment_scene

            self.logger.info(f"Using query length: {len(query)} characters")

            param = self.QueryParam(mode="videoragcontent")
            # if param.wo_reference = False, VideoRAG will add reference to video clips in the response
            param.wo_reference = not use_references

            videoragcontent = self.VideoRAG(working_dir=working_dir)

            response = videoragcontent.query(query=query, param=param)
            self.logger.info("VideoRAG query completed successfully")

            return {"status": "success"}

        except FileNotFoundError:
            self.logger.error(f"Error: JSON file not found at {scene_file}")
            return {
                "status": "failure",
                "error": f"File not found: {scene_file}",
                "matches": [],
            }
        except json.JSONDecodeError:
            self.logger.error("Error: Invalid JSON format in the file.")
            return {"status": "failure", "error": "Invalid JSON format", "matches": []}
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return {"status": "failure", "error": str(e), "matches": []}

    def execute(self, **kwargs):
        """Execute the video search process"""
        # Set up logging
        logging.basicConfig(level=logging.INFO)

        # Validate input parameters
        params = self.InputSchema(**kwargs)

        # Use provided values or defaults
        video_scene_path = params.video_scene_path
        working_dir = self.working_dir
        use_references = False

        # Initialize multiprocessing with spawn method if needed
        try:
            if multiprocessing.get_start_method(allow_none=True) != "spawn":
                multiprocessing.set_start_method("spawn")
        except RuntimeError:
            # This handles the case where the start method has already been set
            pass

        self.logger.info(f"Starting video search using scene file: {video_scene_path}")
        self.logger.info(f"Working directory: {working_dir}")

        # Process the scene and get matching segments
        result = self._process_scene(video_scene_path, working_dir, use_references)

        # Return the structured output
        return {
            "status": result["status"],
        }
