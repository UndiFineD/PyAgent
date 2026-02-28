#!/usr/bin/env python3

"""
Vision agent.py module.
"""
# Copyright 2026 PyAgent Authors
# VisionAgent: Image Analysis and Computer Vision Specialist - Phase 319 Enhanced

from __future__ import annotations

import base64
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


# pylint: disable=too-many-ancestors
class VisionAgent(BaseAgent):
    """
    Agent specializing in image description, OCR, diagram analysis,
    and visual pattern recognition using multi-modal model backends.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Vision Agent. You excel at analyzing visual data, "
            "describing images, extracting text from screenshots or diagrams, "
            "and understanding visual patterns. Be objective, detailed, and structured "
            "in your descriptions. When analyzing code screenshots, extract the actual code."
        )
        self._analysis_cache: Dict[str, Dict] = {}

    @as_tool
    async def analyze_image(self, image_source: str, query: str = "Describe this image in detail.") -> Dict[str, Any]:
        """
        Analyzes an image and answers a query about it.
        image_source: Either a base64 string, file path, or URL.
        """
        b64_data = await self._resolve_image_source(image_source)
        if not b64_data:
            return {"error": "Could not load image", "status": "failed"}

        # Check cache
        cache_key = f"{hash(b64_data[:100])}:{query[:50]}"
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key]

        prompt = f"[IMAGE_DATA:{b64_data}]\n{query}"
        logging.info("VisionAgent: Requesting multi-modal analysis...")

        result = await self.improve_content(prompt)

        response = {"query": query, "description": result, "status": "success"}
        self._analysis_cache[cache_key] = response
        return response

    @as_tool
    async def extract_text_ocr(self, image_source: str) -> Dict[str, Any]:
        """Extracts all visible text from an image (OCR)."""
        b64_data = await self._resolve_image_source(image_source)
        if not b64_data:
            return {"error": "Could not load image", "status": "failed"}

        prompt = (
            f"[IMAGE_DATA:{b64_data}]\n"
            "Extract ALL visible text from this image. "
            "Preserve the layout and formatting as much as possible. "
            "Output only the extracted text, nothing else."
        )

        result = await self.improve_content(prompt)

        return {"extracted_text": result, "word_count": len(result.split()), "status": "success"}

    @as_tool
    async def analyze_code_screenshot(self, image_source: str) -> Dict[str, Any]:
        """Extracts and analyzes code from a screenshot."""
        b64_data = await self._resolve_image_source(image_source)
        if not b64_data:
            return {"error": "Could not load image", "status": "failed"}

        extract_prompt = (
            f"[IMAGE_DATA:{b64_data}]\n"
            "This is a screenshot of code. Extract the exact code shown. "
            "Output ONLY the code with proper indentation, no explanations."
        )
        extracted_code = await self.improve_content(extract_prompt)

        analyze_prompt = (
            "Analyze this code and identify:\n"
            "1. Programming language\n"
            "2. Purpose/functionality\n"
            "3. Any visible issues\n\n"
            f"Code:\n{extracted_code}"
        )
        analysis = await self.improve_content(analyze_prompt)

        # Detect language
        language = "unknown"
        lang_patterns = {
            "python": r"\b(def |import |class |print\()",
            "javascript": r"\b(function |const |let |var |=>)",
            "rust": r"\b(fn |let |mut |impl |struct )",
            "java": r"\b(public |private |class |void |static )",
        }
        for lang, pattern in lang_patterns.items():
            if re.search(pattern, extracted_code):
                language = lang
                break

        return {
            "extracted_code": extracted_code,
            "detected_language": language,
            "analysis": analysis,
            "status": "success",
        }

    @as_tool
    async def analyze_diagram(self, image_source: str, diagram_type: str = "auto") -> Dict[str, Any]:
        """Analyzes flowcharts, UML diagrams, architecture diagrams, etc."""
        b64_data = await self._resolve_image_source(image_source)
        if not b64_data:
            return {"error": "Could not load image", "status": "failed"}

        prompt = (
            f"[IMAGE_DATA:{b64_data}]\n"
            f"Analyze this {'diagram' if diagram_type == 'auto' else diagram_type}. "
            "Identify:\n1. Type of diagram\n2. Main components/nodes\n3. Relationships/connections\n"
            "4. Data flow or sequence (if applicable)\n5. Key insights"
        )

        result = await self.improve_content(prompt)

        return {"diagram_type": diagram_type, "analysis": result, "status": "success"}

    @as_tool
    async def compare_images(self, image1_source: str, image2_source: str) -> Dict[str, Any]:
        """Compares two images and identifies differences."""
        b64_1 = await self._resolve_image_source(image1_source)
        b64_2 = await self._resolve_image_source(image2_source)

        if not b64_1 or not b64_2:
            return {"error": "Could not load one or both images", "status": "failed"}

        prompt = (
            f"[IMAGE_DATA:{b64_1}]\n"
            f"[IMAGE_DATA:{b64_2}]\n"
            "Compare these two images. Identify:\n"
            "1. Key similarities\n2. Key differences\n3. Any notable changes"
        )

        result = await self.improve_content(prompt)

        return {"comparison": result, "status": "success"}

    @as_tool
    async def detect_objects(self, image_source: str, target_objects: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detects and locates objects in an image."""
        b64_data = await self._resolve_image_source(image_source)
        if not b64_data:
            return {"error": "Could not load image", "status": "failed"}

        if target_objects:
            prompt = (
                f"[IMAGE_DATA:{b64_data}]\n"
                f"Locate these objects in the image: {', '.join(target_objects)}\n"
                "For each found object, describe its location (top/bottom, left/right/center)."
            )
        else:
            prompt = (
                f"[IMAGE_DATA:{b64_data}]\n"
                "List all distinct objects visible in this image with their approximate locations."
            )

        result = await self.improve_content(prompt)

        return {"target_objects": target_objects, "detections": result, "status": "success"}

    # pylint: disable=too-many-return-statements
    async def _resolve_image_source(self, source: str) -> Optional[str]:
        """Resolves various image sources to base64."""
        if not source:
            return None

        # Already base64
        if len(source) > 500 and not source.startswith(("http", "/")):
            return source

        # File path
        path = Path(source)
        if path.exists() and path.is_file():
            try:
                with open(path, 'rb') as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except (IOError, OSError, AttributeError) as e:
                logging.error(f"VisionAgent: Failed to read file {source}: {e}")
                return None

        # URL
        if source.startswith(("http://", "https://")):
            from src.infrastructure.security.network.firewall import ReverseProxyFirewall

            firewall = ReverseProxyFirewall()
            try:
                response = firewall.get(source, timeout=10)
                if response.status_code == 200:
                    return base64.b64encode(response.content).decode("utf-8")
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error(f"VisionAgent: Failed to fetch URL {source}: {e}")
                return None

        return source  # Assume it's already base64
