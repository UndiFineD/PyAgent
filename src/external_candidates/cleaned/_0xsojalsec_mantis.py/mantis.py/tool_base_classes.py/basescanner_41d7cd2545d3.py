# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\tool_base_classes\baseScanner.py
from mantis.models.args_model import ArgsModel


class BaseScanner:
    def __init__(self) -> None:
        self.results = {}

    def init(self, args: ArgsModel):
        raise NotImplementedError

    async def execute(self, tooltuple):
        raise NotImplementedError
