# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\load_blueprint.py\client_9cae60b927ed.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\load_blueprint\client.py

from fle.env.entities import Position

from fle.env.tools import Tool


class LoadBlueprint(Tool):
    def __init__(self, *args):

        super().__init__(*args)

    def __call__(self, blueprint: str, position: Position) -> bool:
        """

        Loads a blueprint into the game.

        :param blueprint: Name of the blueprint to load

        :return: True if successful, False otherwise

        """

        assert isinstance(blueprint, str)

        result, _ = self.execute(self.player_index, blueprint, position.x, position.y)

        if result == 0:
            return True

        return False
