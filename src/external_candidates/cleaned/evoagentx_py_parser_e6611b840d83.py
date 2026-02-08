# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\core.py\parser_e6611b840d83.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\core\parser.py

from .module import BaseModule


class Parser(BaseModule):
    @classmethod
    def parse(cls, content: str, **kwargs):
        """

        the method used to parse text into a Parser object. Use Parser.from_str to parse input by default.

        Args:

            content: The content to parse

            **kwargs: Additional keyword arguments

        Returns:

            Parser: The parsed Parser object

        """

        return cls.from_str(content, **kwargs)

    def save(self, path: str, **kwargs) -> str:
        """

        Save the Parser object to a file.

        """

        super().save_module(path, **kwargs)
