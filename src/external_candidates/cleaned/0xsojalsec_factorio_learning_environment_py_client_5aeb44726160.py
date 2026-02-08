# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\get_production_stats.py\client_5aeb44726160.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\get_production_stats\client.py

from fle.env.tools import Tool


class GetProductionStats(Tool):
    def __init__(self, connection, game_state):

        super().__init__(connection, game_state)

        self.name = "production_stats"

        self.game_state = game_state

    def __call__(self, *args, **kwargs):

        response, execution_time = self.execute(self.player_index, *args)

        return response
