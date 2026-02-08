# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\create_agent_characters.py\client_afecae01d9d6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\create_agent_characters\client.py

from fle.env.tools import Tool


class CreateAgentCharacters(Tool):
    def __init__(self, connection, game_state):

        super().__init__(connection, game_state)

    def __call__(self, num_agents: int) -> bool:
        """

        Creates an agent character

        """

        response, elapsed = self.execute(num_agents)

        return True
