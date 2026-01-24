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

"""
Core expansion agent.py module.
"""


from __future__ import annotations

import logging
import subprocess
import sys

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CoreExpansionAgent(BaseAgent):
    """
    Agent responsible for autonomous environment expansion.
    Detects missing libraries and installs them into the active Python environment.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Core Expansion Agent. "
            "Your purpose is to ensure the swarm has the necessary tools and libraries. "
            "When a task fails due to missing dependencies, you are responsible for "
            "identifying the required packages and managing their installation."
        )

    @as_tool
    def install_missing_dependency(self, package_name: str) -> str:
        """
        Attempts to install a missing Python package using pip.
        """
        logging.info(f"CoreExpansionAgent: Attempting to install package: {package_name}")

        try:
            # Use subprocess to run pip
            cmd_str = f"{sys.executable} -m pip install {package_name}"
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                check=True,
            )
            logging.info(f"CoreExpansionAgent: Successfully installed {package_name}")

            # Phase 108: Record intelligence for future dependency graph learning
            self._record(cmd_str, f"Success\n{result.stdout}", provider="Shell", model="pip")

            return f"Success: {package_name} installed.\nStdout: {result.stdout}"
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr or str(e)
            logging.error(f"CoreExpansionAgent: Failed to install {package_name}. Error: {err_msg}")

            # Phase 108: Record failure as a lesson
            self._record(
                f"pip install {package_name}",
                f"Failed: {err_msg}",
                provider="Shell",
                model="pip",
            )

            return f"Error: Failed to install {package_name}. Details: {err_msg}"

    @as_tool
    def audit_environment(self) -> list[str]:
        """
        Lists currently installed packages in the environment.
        """
        try:
            from importlib.metadata import distributions

            return [f"{d.metadata['Name']}=={d.version}" for d in distributions()]
        except (ImportError, KeyError):
            import pkg_resources

            installed_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
            return installed_packages
