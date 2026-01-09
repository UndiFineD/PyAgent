import json
import time
import requests
from typing import Any, Dict, Optional
from pathlib import Path
from src.classes.base_agent.ConnectivityManager import ConnectivityManager
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

class TelemetryAgent:
    """Agent responsible for broadcasting fleet telemetry to the API server."""
    
    def __init__(self, api_url: str = "http://localhost:8000", workspace_root: Optional[str] = None) -> None:
        self.api_url = api_url
        self.log_buffer = []
        
        # Phase 108: Robustness and Intelligence Harvesting
        self.connectivity = ConnectivityManager(workspace_root)
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None

    def _record(self, event_type: str, data: Dict[str, Any]) -> None:
        """Harvest telemetry logic for future self-improvement."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "telemetry", "timestamp": time.time()}
                self.recorder.record_interaction("telemetry", "broadcast", event_type, json.dumps(data), meta=meta)
            except Exception:
                pass

    def log_event(self, event_type: str, source: str, data: Dict[str, Any]) -> None:
        event = {
            "type": event_type,
            "source": source,
            "data": data,
            "timestamp": time.time()
        }
        print(f"[Telemetry] {event_type} from {source}")
        
        # Phase 108: TTL-based connectivity check
        if self.connectivity.is_endpoint_available("telemetry_server"):
            try:
                # requests.post(f"{self.api_url}/telemetry/log", json=event, timeout=0.1)
                # self.connectivity.update_status("telemetry_server", True)
                pass 
            except Exception:
                # self.connectivity.update_status("telemetry_server", False)
                pass
        
        self._record(event_type, data)
        self.log_buffer.append(event)
        if len(self.log_buffer) > 100:
            self.log_buffer.pop(0)

    def get_recent_logs(self) -> List[Dict[str, Any]]:
        return self.log_buffer
