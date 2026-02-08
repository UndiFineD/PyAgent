# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\agent.py\init_f53ecf0843fc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\agent\__init__.py

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def invoke(self, input: str):
        pass

    @abstractmethod
    def stream(self, input: str):
        pass
