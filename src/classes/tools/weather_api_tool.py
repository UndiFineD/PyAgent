import logging
from src.classes.base_agent.utilities import as_tool

class Weather_APITool:
    """Auto-generated tool class"""

    def __init__(self) -> None:
        self.name = 'Weather_API'

    @as_tool
    def get_weather(self, **kwargs) -> dict:
        """Get weather"""
        logging.info(f'Calling GET /weather with {kwargs}')
        return {'path': '/weather', 'method': 'GET', 'result': 'Mocked'}
