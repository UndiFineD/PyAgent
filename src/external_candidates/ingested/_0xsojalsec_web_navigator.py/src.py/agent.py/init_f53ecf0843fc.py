# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\agent\__init__.py
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def invoke(self, input: str):
        pass

    @abstractmethod
    def stream(self, input: str):
        pass
