# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\clear_collision_boxes.py\client_4459d11320b2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\clear_collision_boxes\client.py

from fle.env.tools import Tool


class ClearCollisionBoxes(Tool):
    def __init__(self, connection, game_state):

        super().__init__(connection, game_state)

    def __call__(self) -> bool:
        """

        Removes all pipe insulation

        """

        response, elapsed = self.execute(self.player_index)

        return True
