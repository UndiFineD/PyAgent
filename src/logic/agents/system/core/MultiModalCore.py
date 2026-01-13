
"""
Core logic for Multi-Modal Context (Phase 178).
Handles interactions with vision models for bug analysis.
"""

import base64
from typing import Dict, Any

class MultiModalCore:
    @staticmethod
    def encode_image(image_path: str) -> str:
        """
        Encodes an image file to base64.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def construct_vision_payload(model: str, prompt: str, base64_image: str) -> Dict[str, Any]:
        """
        Constructs a payload for a vision model (OpenAI-style).
        """
        return {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

    @staticmethod
    def parse_bug_report(vision_response: str) -> Dict[str, Any]:
        """
        Simplifies vision response into a structured bug report.
        """
        # Heuristic parsing - in reality, we'd use JSON mode if supported
        is_bug = "bug" in vision_response.lower() or "error" in vision_response.lower()
        return {
            "potential_bug": is_bug,
            "description": vision_response,
            "confidence": 0.85 if is_bug else 0.5
        }