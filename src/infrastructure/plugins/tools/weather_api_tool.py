import logging
from src.core.base.ConnectivityManager import ConnectivityManager
import requests
from src.core.base.utilities import as_tool

class Weather_APITool:
    """Auto-generated tool class"""

    def __init__(self, base_url: str = "http://localhost:8080") -> None:
        self.name = 'Weather_API'
        self.base_url = base_url.rstrip('/')

    @as_tool
    def get_weather(self, **kwargs: Any) -> Any:
        """Get weather"""
        url = f"{self.base_url}/weather"
        try:
            response = requests.request('GET', url, json=kwargs, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Tool get_weather failed: {e}")
            return {"error": str(e), "path": '/weather', "method": 'GET'}
