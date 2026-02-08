# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\agent.py\set_research.py\client_b479edfd1f3f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\agent\set_research\client.py

from typing import List, Optional

from fle.env.game_types import Technology

from fle.env.tools import Tool

from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str

    count: Optional[int] = 1

    type: Optional[str] = None


class SetResearch(Tool):
    def __init__(self, connection, game_state):
        super().__init__(connection, game_state)

    def __call__(self, technology: Technology) -> List[Ingredient]:
        """

        Set the current research technology for the player's force.

        :param technology: Technology to research

        :return: Required ingredients to research the technology.

        """

        if hasattr(technology, "value"):
            name = technology.value

        else:
            name = technology

        success, elapsed = self.execute(self.player_index, name)

        if success != {} and isinstance(success, str):
            if success is None:
                raise Exception(f"Could not set research to {name} - Technology is invalid or unavailable.")

            else:
                result = ":".join(success.split(":")[2:]).replace('"', "").strip()

                if not result:
                    raise Exception(f"Could not set research to {name} - {success}")

                else:
                    raise Exception(result)

        # Parse the returned ingredients list

        if isinstance(success, list):
            return [
                Ingredient(
                    name=ingredient.get("name"),
                    count=ingredient.get("count", 1),
                    type=ingredient.get("type"),
                )
                for ingredient in success
            ]

        # Fallback empty list if no ingredients returned

        return []
