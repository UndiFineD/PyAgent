# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\capability\app_capability.py
from abc import ABC, abstractmethod

from fastapi import FastAPI


class ApplicationCapability(ABC):
    @abstractmethod
    def enable(self, app: FastAPI):
        pass
