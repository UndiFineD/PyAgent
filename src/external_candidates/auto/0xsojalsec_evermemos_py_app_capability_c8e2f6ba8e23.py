# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\capability.py\app_capability_c8e2f6ba8e23.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\capability\app_capability.py

from abc import ABC, abstractmethod

from fastapi import FastAPI

class ApplicationCapability(ABC):

    @abstractmethod

    def enable(self, app: FastAPI):

        pass

