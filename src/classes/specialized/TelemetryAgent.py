import json
import time
import requests
from typing import Any, Dict

class TelemetryAgent:
    """Agent responsible for broadcasting fleet telemetry to the API server."""
    
    def __init__(self, api_url: str = "http://localhost:8000") -> None:
        self.api_url = api_url
        self.log_buffer = []

    def log_event(self, event_type: str, source: str, data: Dict[str, Any]):
        event = {
            "type": event_type,
            "source": source,
            "data": data,
            "timestamp": time.time()
        }
        print(f"[Telemetry] {event_type} from {source}")
        
        # In a real async environment, we would use a WebSocket client or async post.
        # For simulation, we'll try to post to a local endpoint if it's up.
        try:
            # Non-blocking-ish or fire-and-forget logic would be better
            # requests.post(f"{self.api_url}/telemetry/log", json=event, timeout=0.1)
            pass 
        except Exception:
            pass
        
        self.log_buffer.append(event)
        if len(self.log_buffer) > 100:
            self.log_buffer.pop(0)

    def get_recent_logs(self):
        return self.log_buffer
