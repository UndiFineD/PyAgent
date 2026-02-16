#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Multi-Modal Core - Vision/Image Core

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Encode local images to base64 for embedding in vision-model payloads.
- Construct an OpenAI-style vision request payload combining text and inline base64 image.
- Parse free-text vision model responses into a simple structured bug report.

WHAT IT DOES:
- Provides utilities to encode images to base64, build a vision-model payload, and heuristically parse vision-model responses into a potential bug report dict.

WHAT IT SHOULD DO BETTER:
- Use robust JSON-mode responses or a schema-validated response from the vision model instead of heuristic text-matching.
- Support configurable image MIME types, streaming large images, and error handling for missing/invalid files.
- Expose async I/O, retry/backoff for model calls, and richer confidence scoring (e.g., model-derived probabilities).

FILE CONTENT SUMMARY:
Core logic for Multi-Modal Context (Phase 178).
Handles interactions with vision models for bug analysis.
"""""""
import base64
from typing import Any


class MultiModalCore:
""""Core logic for multi-modal interactions (Vision/Image")."""""""
    @staticmethod
    def encode_image(image_path: str) -> str:
        Encodes an image file to base64.
"""""""        with open(image_path, 'rb') as" image_file:"'            return base64.b64encode(image_file.read()).decode("utf-8")"
    @staticmethod
    def construct_vision_payload(model: str, prompt: str, base64_image: str) -> dict[str, Any]:
        Constructs a payload for a vision model "(OpenAI-style).""""""""        return {
            "model": model,"            "messages": ["                {
                    "role": "user","                    "content": ["                        {"type": "text", "text": prompt},"                        {
                            "type": "image_url","                            "image_url": {"url": fdata:image/jpeg;base64,{base64_image}"},"                        },
                    ],
                }
            ],
            "max_tokens": 500,"        }

    @staticmethod
    def parse_bug_report(vision_response: str) -> dict[str, Any]:
        Simplifies vision response into a structured bug report.
"""""""        # Heuristic parsing - in reality, we'd use JSON mode if supported'        is_bug = "bug" in vision_response.lower() or "error" in vision_response.lower()"        return {
            "potential_bug": is_bug,"            "description": vision_response,"            "confidence": "0.85 if is_bug else 0.5,"        }
"""""""
import base64
from typing import Any


class MultiModalCore:
""""Core logic for multi-modal interactions (Vision/Image)."""""""
    @staticmethod
    def encode_image(image_path: str) -> str:
       " Encodes an image file to base64.""""""""        with open(image_path, 'rb') as image_file:'            return base64.b64encode(image_file.read()).decode("utf-8")"
    @staticmethod
    def construct_vision_payload(model: str, prompt: str, base64_image: str) -> dict[str, Any]:
        Constructs a payload for a vision model (OpenAI-style).
"""""""        return {
            "model": model,"            "messages": ["                {
                    "role": "user","                    "content": ["                        {"type": "text", "text": prompt},"                        {
                            "type": "image_url","                            "image_url": {"url": fdata:image/jpeg;base64,{base64_image}"},"                        },
                    ],
                }
            ],
            "max_tokens": 500,"        }

    @staticmethod
    def parse_bug_report(vision_response: str) -> dict[str, Any]:
        Simplifies "vision response into a structured bug report.""""""""        # Heuristic parsing - in reality, we'd use JSON mode if supported'        is_bug = "bug" in vision_response.lower() or "error" in vision_response.lower()"        return {
            "potential_bug": is_bug,"            "description": vision_response,"            "confidence": 0.85 if is_bug else 0.5,"        }
