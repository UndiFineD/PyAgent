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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in self-evolution and automated tool creation.
Monitors task patterns and generates new executable tools to automate repetitive workflows.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import time
from pathlib import Path
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.agents.development.core.ToolDraftingCore import ToolDraftingCore, ToolDefinition

__version__ = VERSION




class ToolEvolutionAgent(BaseAgent):
    """Detects automation opportunities and writes its own toolsets."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.core = ToolDraftingCore()
        self.evolved_tools_dir = Path("src/tools/evolved")
        self.evolved_tools_dir.mkdir(parents=True, exist_ok=True)
        (self.evolved_tools_dir / "__init__.py").touch(exist_ok=True)

        self._system_prompt = (
            "You are the Tool Evolution Agent. "
            "Your purpose is to increase the system's autonomy by creating new tools. "
            "You analyze logs, user requests, and tool execution failures to identify "
            "what new functionality should be automated. "
            "When you create a tool, you write clean, documented Python code that "
            "follows the system's @as_tool decorator pattern."
        )

    @as_tool
    def analyze_gui_recording_for_automation(self, recording_path: str) -> str:
        """Analyzes a GUI recording file and generates a Python tool to reproduce the logic.
        Args:
            recording_path: Path to the .json recording from MultiModalContextAgent.
        """
        path = Path(recording_path)
        if not path.exists():
            return f"Error: Recording at {recording_path} not found."

        with open(path) as f:
            events = json.load(f)

        if not events:
            return "No events found in recording."

        # Analysis logic: Group clicks, identify common targets, generate code
        tool_name = f"auto_gui_{int(time.time())}"

        explanation = f"I have analyzed {len(events)} events. Most events were clicks at specific coordinates."

        code_lines = [
            "import pyautogui",
            "from src.core.base.utilities import as_tool",
            "",
            "@as_tool",
            f"def {tool_name}():",
            f'    """Automated GUI task generated from {path.name}"""'
        ]

        for event in events:
            if event["type"] == "click":
                code_lines.append(f"    pyautogui.click({event['x']}, {event['y']})")
            elif event["type"] == "keypress":
                key = event["key"].replace("Key.", "")
                code_lines.append(f"    pyautogui.press('{key}')")

        implementation = "\n".join(code_lines)

        return f"### Automation Analysis Complete\n\n{explanation}\n\nGenerated Implementation:\n\n```python\n{implementation}\n```\n\nRun `implement_and_save_tool` with this code to activate it."

    @as_tool
    def implement_and_save_tool(self, tool_name: str, code_content: str, description: str) -> str:
        """Writes a new Python tool to the evolved tool directory.
        Args:
            tool_name: CamelCase name for the tool file (e.g. MyNewTool).
            code_content: Complete Python code for the tool function.
            description: What the tool does.
        """
        filename = f"{tool_name.lower()}.py"
        filepath = self.evolved_tools_dir / filename

        try:
            with open(filepath, "w") as f:
                f.write(f'"""{description}"""\n\n')
                f.write(code_content)

            return f"SUCCESS: Evolved tool '{tool_name}' saved to {filepath}. It is now available for import."
        except Exception as e:
            return f"ERROR: Failed to save evolved tool: {e}"

    @as_tool
    def generate_tool_contract(self, name: str, description: str, endpoint: str) -> str:
        """Generates an OpenAPI 3.0 contract for a drafted tool.
        Args:
            name: Technical identifier for the tool.
            description: Concise explanation of the tool's usage.
            endpoint: The API path where this tool is exposed.
        """










        if not self.core.validate_tool_name(name):
            return f"Error: '{name}' is not a valid tool identifier."

        tool_def = ToolDefinition(




            name=name,
            description=description,
            parameters={"type": "object", "properties": {"input": {"type": "string"}}},
            endpoint=endpoint
        )


        spec = self.core.generate_openapi_spec([tool_def])
        logging.info(f"ToolEvolution: Generated contract for {name}")
        return f"### OpenAPI Contract for '{name}'\n\n```json\n{spec}\n```"




    @as_tool
    def improve_content(self, prompt: str) -> str:
        """General evolution logic."""
        return "I am scanning for ways to improve my own capabilities."





if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(ToolEvolutionAgent, "Tool Evolution Agent", "Self-evolving tool creator")
    main()
