# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\tools.py\interpreter_base_f75da85c03cf.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\tools\interpreter_base.py

from ..core.module import BaseModule


class BaseInterpreter(BaseModule):
    """

    Base class for interpreter tools that execute code securely.

    Provides common functionality for interpreter operations.

    """

    def __init__(self, name: str = "BaseInterpreter", **kwargs):
        super().__init__(name=name, **kwargs)
