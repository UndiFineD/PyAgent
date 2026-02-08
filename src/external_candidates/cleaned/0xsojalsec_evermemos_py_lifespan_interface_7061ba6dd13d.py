# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\lifespan.py\lifespan_interface_7061ba6dd13d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\lifespan\lifespan_interface.py

"""

FastAPI lifespan interface definition

Simple lifespan management interface that supports ordering and name field definition

"""

from abc import ABC, abstractmethod

from typing import Any

from fastapi import FastAPI

from core.observation.logger import get_logger

logger = get_logger(__name__)


class LifespanProvider(ABC):
    """Lifespan provider interface"""

    def __init__(self, name: str, order: int = 0):
        """

        Initialize lifespan provider

        Args:

            name (str): Provider name

            order (int): Execution order, smaller numbers execute first

        """

        self.name = name

        self.order = order

    @abstractmethod
    async def startup(self, app: FastAPI) -> Any:
        """Startup logic"""

        ...

    @abstractmethod
    async def shutdown(self, app: FastAPI) -> None:
        """Shutdown logic"""

        ...
