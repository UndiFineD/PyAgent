#!/usr/bin/env python3

"""Agent specializing in 2D SVG image generation and optimization."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class SvgAgent(CoderAgent):
    """Agent for generating and optimizing 2D SVG vector graphics."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "xml" # SVG is XML-based
        self._system_prompt = (
            "You are an SVG Graphic Designer and Vector Optimization Expert. "
            "You generate high-quality, clean, and optimized 2D SVG code. "
            "Focus on semantic tags, proper viewports, path optimization, and CSS styling within the SVG. "
            "Avoid bloated markup and use minimal precision for coordinates."
        )

    def _get_default_content(self) -> str:
        return "<svg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\">\n  <circle cx=\"50\" cy=\"50\" r=\"40\" stroke=\"black\" stroke-width=\"3\" fill=\"red\" />\n</svg>\n"

if __name__ == "__main__":
    main = create_main_function(SvgAgent, "SVG Agent", "Path to SVG file (.svg)")
    main()
