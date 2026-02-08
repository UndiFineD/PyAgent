# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent_serve.py\service_instance_95f0344bcbdc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent_serve\service_instance.py

from .service import Service

from .service_manager import ServiceManager


class ServiceNotFoundError(Exception):
    """An exception when service code is not in service manager."""

    def __init__(self, service_code: str):
        super().__init__(f"Service {service_code} not found.")

        self.service_code = service_code


class ServiceInstance(object):
    """A service wrapper class, which should be directly called in project

    instead of Service class."""

    def __init__(self, service_code: str):
        """Initialize a service instance. Raise an ServiceNotFoundError when

        service code can't be found by service manager.

        Args:

            service_code (`str`):

                Unique code of the service.

        """

        self.__service_code = service_code

        service_manager: ServiceManager = ServiceManager()

        self.__service: Service = service_manager.get_instance_obj(service_code)

        if self.__service is None:
            raise ServiceNotFoundError(service_code)

    def run(self, **kwargs) -> str:
        """Call the service run."""

        return self.__service.run(**kwargs)
