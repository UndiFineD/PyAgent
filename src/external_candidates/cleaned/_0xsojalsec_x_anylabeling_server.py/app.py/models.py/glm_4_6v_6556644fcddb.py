# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\models\glm_4_6v.py
import ast
import base64
import json
import os
import re
from io import BytesIO
from typing import Any, Dict

import numpy as np
from app.core.registry import register_model
from app.schemas.shape import Shape
from loguru import logger
from PIL import Image

from . import BaseModel


@register_model(
    "glm_4_6v_grounding_api",
)
class GLM46V(BaseModel):
    """GLM-4.6V model supporting grounding tasks via ZaiClient API."""

    def load(self):
        """Load GLM-4.6V model using ZaiClient API."""
        self.api_key = self.params.get("api_key") or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set api_key in params or ZHIPU_API_KEY environment variable.")
        self.model_name = self.params.get("model_name", "glm-4.6v")
        self.default_task = self.params.get("task", "grounding")
        logger.info(f"Using GLM-4.6V API backend with model {self.model_name}")

    def predict(self, image: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute prediction based on task type.

        Args:
            image: Input image in BGR format.
            params: Inference parameters including task type.

        Returns:
            Dictionary with prediction results.
        """
        task = params.get("task", self.default_task)

        if task == "grounding":
            return self._predict_grounding(image, params)
        else:
            raise ValueError(f"Unsupported task: {task}")

    def _predict_caption(self, image: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute image captioning task."""
        prompt_mode = params.get("prompt_mode", "brief")

        if prompt_mode == "detailed":
            prompt = (
                "Describe this image in detail. Include information about: "
                "the main subjects and objects, their positions and relationships, "
                "colors, lighting, background, activities or actions taking place, "
                "and the overall scene or context."
            )
        elif prompt_mode == "brief":
            prompt = "Provide a brief, concise description of this image."
        else:
            prompt = params.get("custom_prompt", "Describe what you see in this image.")

        description = self._inference_api(image, prompt, params)
        logger.info(f"Generated caption: {description[:200]}...")

        return {"shapes": [], "description": description}

    def _predict_grounding(self, image: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute 2D object grounding task."""
        text_prompt = params.get("text_prompt", "")
        if not text_prompt:
            logger.warning("Please provide a text prompt for grounding task.")
            return {"shapes": [], "description": ""}

        categories_list = [cat.strip() for cat in text_prompt.split(".") if cat.strip()]
        categories = ", ".join(categories_list)

        prompt = (
            f"Identify all instances of the specified target categories {categories} in the image. "
            "Return the results in valid JSON format as a list, where each element is a dictionary "
            'with keys "label" and "bbox_2d". The "label" value must be one of the class names from '
            f'the input list {categories}, and "bbox_2d" must be a list of four integers [x1, y1, x2, y2] '
            'representing the bounding box coordinates. For example: [{"label": "cat", "bbox_2d": [1,2,3,4]}, '
            '{"label": "dog", "bbox_2d": [5,6,7,8]}]'
        )

        response = self._inference_api(image, prompt, params)
        shapes = self._parse_grounding_response(response, image.shape)

        return {"shapes": shapes, "description": ""}

    def _inference_api(self, image: np.ndarray, prompt: str, params: Dict[str, Any]) -> str:
        """Run inference using ZaiClient API."""
        from zai import ZaiClient

        max_tokens = params.get("max_tokens", self.params.get("max_tokens", 2048))
        temperature = params.get("temperature", self.params.get("temperature", 0.7))

        pil_image = Image.fromarray(image[:, :, ::-1])
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        img_data_uri = f"data:image/png;base64,{img_base64}"

        client = ZaiClient(api_key=self.api_key)

        request_params = {
            "model": self.model_name,
            "messages": [
                {
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": img_data_uri},
                        },
                        {"type": "text", "text": prompt},
                    ],
                    "role": "user",
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        thinking_enabled = params.get("thinking", self.params.get("thinking", False))
        if thinking_enabled:
            request_params["thinking"] = {"type": "enabled"}

        try:
            response = client.chat.completions.create(**request_params)
            content = response.choices[0].message.content
            return content.strip()
        except Exception as e:
            logger.error(f"ZaiClient API inference error: {e}")
            raise

    @staticmethod
    def _parse_json(json_output: str) -> str:
        """Parse JSON output from model, removing markdown fencing."""
        lines = json_output.splitlines()
        for i, line in enumerate(lines):
            if line == "```json":
                json_output = "\n".join(lines[i + 1 :])
                json_output = json_output.split("```")[0]
                break
        return json_output

    @staticmethod
    def _extract_json_from_response(response: str) -> str:
        """Extract JSON content from GLM response with markers."""
        begin_marker = "<|begin_of_box|>"
        end_marker = "<|end_of_box|>"

        begin_idx = response.find(begin_marker)
        end_idx = response.find(end_marker)

        if begin_idx != -1 and end_idx != -1:
            json_content = response[begin_idx + len(begin_marker) : end_idx].strip()
            return json_content

        pattern = r'\[\s*\{[^}]*"label"[^}]*"bbox_2d"[^}]*\}(?:\s*,\s*\{[^}]*"label"[^}]*"bbox_2d"[^}]*\})*\s*\]'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(0)

        bracket_start = response.find("[")
        if bracket_start != -1:
            bracket_end = response.rfind("]")
            if bracket_end != -1 and bracket_end > bracket_start:
                return response[bracket_start : bracket_end + 1]

        return response.strip()

    def _parse_grounding_response(self, response: str, image_shape: tuple) -> list:
        """Parse grounding response and convert to shapes."""
        shapes = []
        height, width = image_shape[:2]

        logger.info(f"response: {response}")

        json_content = self._extract_json_from_response(response)
        json_content = self._parse_json(json_content)

        try:
            bounding_boxes = json.loads(json_content)
        except json.JSONDecodeError:
            try:
                bounding_boxes = ast.literal_eval(json_content)
            except (ValueError, SyntaxError):
                try:
                    end_idx = json_content.rfind('"}') + len('"}')
                    truncated_text = json_content[:end_idx] + "]"
                    bounding_boxes = json.loads(truncated_text)
                except Exception:
                    try:
                        bounding_boxes = ast.literal_eval(truncated_text)
                    except Exception:
                        return shapes

        if not isinstance(bounding_boxes, list):
            bounding_boxes = [bounding_boxes]

        for bbox_data in bounding_boxes:
            if "bbox_2d" not in bbox_data:
                continue

            bbox = bbox_data["bbox_2d"]
            label = bbox_data.get("label", "object")

            abs_x1 = int(bbox[0] / 1000 * width)
            abs_y1 = int(bbox[1] / 1000 * height)
            abs_x2 = int(bbox[2] / 1000 * width)
            abs_y2 = int(bbox[3] / 1000 * height)

            if abs_x1 > abs_x2:
                abs_x1, abs_x2 = abs_x2, abs_x1
            if abs_y1 > abs_y2:
                abs_y1, abs_y2 = abs_y2, abs_y1

            shape = Shape(
                label=label,
                shape_type="rectangle",
                points=[
                    [float(abs_x1), float(abs_y1)],
                    [float(abs_x2), float(abs_y1)],
                    [float(abs_x2), float(abs_y2)],
                    [float(abs_x1), float(abs_y2)],
                ],
            )
            shapes.append(shape)

        return shapes

    def unload(self):
        """Release model resources."""
        if hasattr(self, "client"):
            del self.client
