# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\tools.py\admin.py\render_message.py\client_b05002abbf27.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\admin\render_message\client.py

from fle.env.tools import Tool


class RenderMessage(Tool):
    def __init__(self, connection, game_state):

        super().__init__(connection, game_state)

        self.name = "render_message"

        self.game_state = game_state

        self.load()

    def __call__(self, message: str) -> bool:
        """

        Render a message in the game chat.

        :param message: The message text to display

        :return: True if successful, raises exception if not

        """

        try:
            # Execute the server command with positional arguments

            response = self.execute(self.player_index, message)

            if isinstance(response, str):
                raise Exception(f"Could not render message: {response}")

            return True

        except Exception as e:
            raise Exception(f"Error rendering message: {str(e)}")
