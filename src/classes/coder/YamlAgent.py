#!/usr/bin/env python3

"""Agent specializing in YAML configuration files."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class YamlAgent(CoderAgent):
    """Agent for YAML configuration improvement."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "yaml"
        self._system_prompt = (
            "You are a YAML and DevOps Configuration Expert. "
            "Focus on clean structure, proper indentation, use of anchors/aliases where helpful, "
            "and adherence to specific schemas (Kubernetes, Docker Compose, CI/CD pipelines). "
            "Ensure the YAML is valid and optimized for machine readability."
        )

    def _get_default_content(self) -> str:
        return "version: '1.0'\nservices:\n  app:\n    image: baseline\n"

if __name__ == "__main__":
    main = create_main_function(YamlAgent, "YAML Agent", "Path to YAML file (.yaml, .yml)")
    main()

