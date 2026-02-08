# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\agent.py\get_research_progress.py\client_ab9207fc2452.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\agent\get_research_progress\client.py

from typing import List, Optional

from fle.env import Ingredient

from fle.env.game_types import Technology

from fle.env.tools import Tool


class GetResearchProgress(Tool):
    def __init__(self, connection, game_state):
        super().__init__(connection, game_state)

    def __call__(self, technology: Optional[Technology] = None) -> List[Ingredient]:
        """

        Get the progress of research for a specific technology or the current research.

        :param technology: Optional technology to check. If None, checks current research.

        :return The remaining ingredients to complete the research

        """

        if technology is not None:
            if hasattr(technology, "value"):
                name = technology.value

            else:
                name = technology

        else:
            name = None

        success, elapsed = self.execute(self.player_index, name)

        if success != {} and isinstance(success, str):
            if success is None:
                raise Exception("No research in progress" if name is None else f"Cannot get progress for {name}")

            else:
                result = ":".join(success.split(":")[2:]).replace('"', "").strip()

                if result:
                    raise Exception(result)

                else:
                    raise Exception(success)

        return [
            Ingredient(
                name=ingredient["name"],
                count=ingredient["count"],
                type=ingredient.get("type"),
            )
            for ingredient in success
        ]
