# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit_prompting.py\src.py\agentkit.py\exceptions_a45caebc1430.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit_prompting\src\agentkit\exceptions.py


class AfterQueryError(Exception):
    """Exception raised for errors in the after query postprocessing.

    Attributes:

        error (str): Error message.

    """

    def __init__(self, message, error):
        """Initializes the AfterQueryError class.

        Args:

            message (str): System error message.

            error (str): Error message for the LLM (a more descriptive error message for LLM to understand)

        """

        # Call the base class constructor with the parameters it needs

        super().__init__(message)

        # Set the error message

        self.error = error
