#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Agent specializing in 2D SVG image generation and optimization."""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.BaseUtilities import create_main_function

__version__ = VERSION


class SvgAgent(CoderAgent):
    """Agent for generating and optimizing 2D SVG vector graphics."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "xml"  # SVG is XML-based

        self._system_prompt = (
            "You are an SVG Graphic Designer and Vector Optimization Expert. "
            "You generate high-quality, clean, and optimized 2D SVG code. "
            "Focus on semantic tags, proper viewports, path optimization, and CSS styling within the SVG. "
            "Avoid bloated markup and use minimal precision for coordinates."
        )

    def _get_default_content(self) -> str:
        return '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">\n  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />\n</svg>\n'


if __name__ == "__main__":
    main = create_main_function(SvgAgent, "SVG Agent", "Path to SVG file (.svg)")
    main()
