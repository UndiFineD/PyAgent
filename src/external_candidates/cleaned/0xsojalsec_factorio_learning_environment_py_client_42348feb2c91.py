# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\save_blueprint.py\client_42348feb2c91.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\save_blueprint\client.py

from typing import Tuple

from fle.env.entities import Position

from fle.env.tools import Tool


class SaveBlueprint(Tool):
    def __init__(self, *args):
        super().__init__(*args)

    def __call__(self) -> Tuple[str, Position]:
        """

        Saves the current player entities on the map into a blueprint string

        :return: Blueprint and offset to blueprint from the origin.

        """

        result, _ = self.execute(self.player_index)

        blueprint = result["blueprint"]

        offset = Position(x=result["center_x"], y=result["center_y"])

        return blueprint, offset
