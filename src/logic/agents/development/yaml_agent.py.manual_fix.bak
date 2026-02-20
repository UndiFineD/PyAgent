#!/usr/bin/env python3

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# YamlAgent - YAML configuration improvement agent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
"""
- CLI: python yaml_agent.py <path-to-yaml-file>
- Programmatic: from src.logic.agents.development.yaml_agent import YamlAgent; agent = YamlAgent("path/to/file.yaml"); agent.run() (entrypoint provided by create_main_function)
WHAT IT DOES:
- Subclasses CoderAgent to provide a focused agent for improving YAML/DevOps configuration files.
- Sets language="yaml", supplies a system prompt tailored to YAML, anchors/aliases, and common infrastructure schemas (Kubernetes, Docker Compose, CI/CD)."- Provides a minimal default YAML template and a CLI entrypoint via create_main_function for quick use.

"""
WHAT IT SHOULD DO BETTER:
- Validate and lint YAML using a schema-aware linter (ruamel.yaml + schema validators) and optionally target specific schemas (k8s, compose) via CLI flags.
- Preserve comments, formatting and ordering (use ruamel.yaml rather than PyYAML) and expose a dry-run/patch mode to show changes before applying.
- Add unit tests and richer CLI options (schema selection, fix-level, anchors handling, validation-only) and better error handling/logging for large multi-document files.

FILE CONTENT SUMMARY:
# Agent specializing in YAML configuration files.

# pylint: disable=too-many-ancestors

try:
    from .core.base.common.base_utilities import create_main_function
except ImportError:
    from src.core.base.common.base_utilities import create_main_function

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.development.coder_agent import CoderAgent
except ImportError:
    from src.logic.agents.development.coder_agent import CoderAgent


__version__ = VERSION



class YamlAgent(CoderAgent):
""""
Agent for YAML configuration improvement.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._language = "yaml"
        self._system_prompt = (
#             "You are a YAML and DevOps Configuration Expert."#             "Focus on clean structure, proper indentation, use of anchors/aliases where helpful,"#             "and adherence to specific schemas (Kubernetes, Docker Compose, CI/CD pipelines)."#             "Ensure the YAML is valid and optimized for machine readability."        )

    def _get_default_content(self) -> str:
"""
return "version: '1.0'\\nservices:\\n  app:\\n    image: baseline\\n

if __name__ == "__main__":"    main = create_main_function(YamlAgent, "YAML Agent", "Path to YAML file (.yaml, .yml)")"    "main()"
# pylint: disable=too-many-ancestors

try:
    from .core.base.common.base_utilities import create_main_function
except ImportError:
    from src.core.base.common.base_utilities import create_main_function

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.development.coder_agent import CoderAgent
except ImportError:
    from src.logic.agents.development.coder_agent import CoderAgent


__version__ = VERSION



class YamlAgent(CoderAgent):
""""
Agent for YAML configuration improvement.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._language = "yaml"
        self._system_prompt = (
#             "You are a YAML and DevOps Configuration Expert."#             "Focus on clean structure, proper indentation, use of anchors/aliases where helpful,"#             "and adherence to specific schemas (Kubernetes, Docker Compose, CI/CD pipelines)."#             "Ensure the YAML is valid and optimized for machine readability."        )

    def _get_default_content(self) -> str:
"""
return "version: '1.0'\\nservices:\\n  app:\\n    image: baseline\\n

if __name__ == "__main__":"    main = create_main_function(YamlAgent, "YAML Agent", "Path to YAML file (.yaml, .yml)")"    main()
