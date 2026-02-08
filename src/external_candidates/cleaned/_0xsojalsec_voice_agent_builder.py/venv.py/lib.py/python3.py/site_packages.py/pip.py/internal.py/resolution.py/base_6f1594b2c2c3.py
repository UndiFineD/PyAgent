# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_internal\resolution\base.py
from typing import Callable, List, Optional

from pip._internal.req.req_install import InstallRequirement
from pip._internal.req.req_set import RequirementSet

InstallRequirementProvider = Callable[[str, Optional[InstallRequirement]], InstallRequirement]


class BaseResolver:
    def resolve(self, root_reqs: List[InstallRequirement], check_supported_wheels: bool) -> RequirementSet:
        raise NotImplementedError()

    def get_installation_order(self, req_set: RequirementSet) -> List[InstallRequirement]:
        raise NotImplementedError()
