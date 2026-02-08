# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\set_inventory.py\client_6937650998c1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\set_inventory\client.py

import json

from typing import Any, Dict

from fle.env.tools import Tool


class SetInventory(Tool):
    def __init__(self, connection, game_state):
        super().__init__(connection, game_state)

    def __call__(self, inventory: Dict[str, Any]) -> bool:
        """

        Sets the inventory for an agent character

        """

        inventory_json = json.dumps(inventory)

        response, elapsed = self.execute(self.player_index, inventory_json)

        return True
