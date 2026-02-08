# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent_serve.py\service_manager_ee9eb9e95336.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent_serve\service_manager.py

from ..base.annotation.singleton import singleton

from ..base.component.component_enum import ComponentEnum

from ..base.component.component_manager_base import ComponentManagerBase

from .service import Service


@singleton
class ServiceManager(ComponentManagerBase[Service]):
    """A singleton manager class of the service."""

    def __init__(self):
        super().__init__(ComponentEnum.SERVICE)
