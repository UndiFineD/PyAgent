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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in YAML configuration files."""




from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
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

