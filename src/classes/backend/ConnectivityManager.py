import time
import logging
from typing import Dict

class ConnectivityManager:
    """
    Centralized connection state management with TTL-based caching.
    Prevents swarm timeout-cascades by tracking health of external endpoints.
    """
    _instance = None
    _statuses: Dict[str, Dict] = {}
    TTL = 900  # 15 minutes

    def __new__(cls) -> bool:
        if cls._instance is None:
            cls._instance = super(ConnectivityManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def is_online(cls, endpoint: str) -> bool:
        """Checks if an endpoint is known to be online within the TTL."""
        status = cls._statuses.get(endpoint)
        if status and (time.time() - status['timestamp'] < cls.TTL):
            return status['online']
        return True # Assume online if unknown

    @classmethod
    def set_status(cls, endpoint: str, online: bool) -> None:
        """Updates the status of an endpoint with a new timestamp."""
        cls._statuses[endpoint] = {
            'online': online,
            'timestamp': time.time()
        }
        if not online:
            logging.warning(f"ConnectivityManager: Endpoint {endpoint} flagged as OFFLINE.")
        else:
            logging.info(f"ConnectivityManager: Endpoint {endpoint} confirmed ONLINE.")
