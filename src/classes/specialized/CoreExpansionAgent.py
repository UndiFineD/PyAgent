#!/usr/bin/env python3

import logging
import subprocess
import sys
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

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
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                check=True
            )
            logging.info(f"CoreExpansionAgent: Successfully installed {package_name}")
            return f"Success: {package_name} installed.\nStdout: {result.stdout}"
        except subprocess.CalledProcessError as e:
            logging.error(f"CoreExpansionAgent: Failed to install {package_name}. Error: {e.stderr}")
            return f"Error: Failed to install {package_name}. Details: {e.stderr}"

    @as_tool
    def audit_environment(self) -> List[str]:
        """
        Lists currently installed packages in the environment.
        """
        import pkg_resources
        installed_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
        return installed_packages
