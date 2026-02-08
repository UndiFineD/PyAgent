# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\reset.py\client_213ac9729056.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\reset\client.py

import json

from fle.env.tools import Tool


class Reset(Tool):
    def __init__(self, connection, game_state):

        super().__init__(connection, game_state)

    def __call__(
        self,
        inventories=None,
        reset_position=False,
        all_technologies_researched=True,
        clear_entities=True,
    ):
        """

        Reset the Factorio game state via Lua action, mirroring FactorioInstance.reset/_reset.

        Args:

                inventories (list[dict]|dict|None): Either a list indexed by agent (1-based in Lua)

                    or a dict keyed by agent index (int or str) mapping to {item_name: count}.

                reset_position (bool): If True, teleport agents to spawn offsets.

                all_technologies_researched (bool): If True, research all technologies; else reset force.

        """

        if inventories is None:
            inventories = {}

        dict_inventories = []

        for inv in inventories:
            if not isinstance(inv, dict):
                dict_inventories.append(inv.__dict__)

            else:
                dict_inventories.append(inv)

        # Encode to JSON string for Lua

        inventories_json = json.dumps(dict_inventories)

        response, _ = self.execute(
            inventories_json,
            reset_position,
            all_technologies_researched,
            clear_entities,
        )

        return response
