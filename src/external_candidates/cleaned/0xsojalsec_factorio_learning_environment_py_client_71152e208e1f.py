# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\extend_collision_boxes.py\client_71152e208e1f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\extend_collision_boxes\client.py

from fle.env.entities import Position

from fle.env.tools import Tool


class ExtendCollisionBoxes(Tool):
    def __init__(self, connection, game_state):
        super().__init__(connection, game_state)

    def __call__(self, source_position: Position, target_position: Position) -> bool:
        """

        Add an insulative buffer of invisible objects around all pipes within the bounding box.

        This is necessary when making other pipe connections, as adjacency can inadvertently cause different

        pipe groups to merge

        """

        response, elapsed = self.execute(
            self.player_index,
            source_position.x,
            source_position.y,
            target_position.x,
            target_position.y,
        )

        return True
