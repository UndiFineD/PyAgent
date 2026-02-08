# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_mantis.py\mantis.py\tool_base_classes.py\basescanner_41d7cd2545d3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\tool_base_classes\baseScanner.py

from mantis.models.args_model import ArgsModel


class BaseScanner:
    def __init__(self) -> None:
        self.results = {}

    def init(self, args: ArgsModel):
        raise NotImplementedError

    async def execute(self, tooltuple):
        raise NotImplementedError
