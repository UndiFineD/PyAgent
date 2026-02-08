# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\action.py\_2_engineering_team.py\engineering_team.py\src.py\engineering_team.py\tools.py\custom_tool_8316a79134e1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\action\2_engineering_team\engineering_team\src\engineering_team\tools\custom_tool.py

from typing import Type

from crewai.tools import BaseTool

from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"

    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )

    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here

        return "this is an example of a tool output, ignore it and move along."
