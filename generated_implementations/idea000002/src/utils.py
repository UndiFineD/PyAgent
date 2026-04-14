"""Utility functions
"""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def serialize(obj: Any) -> str:
    """Serialize object to JSON"""
    return json.dumps(obj, default=str)

def deserialize(data: str) -> Any:
    """Deserialize JSON to object"""
    return json.loads(data)

def log_operation(operation: str, **kwargs):
    """Log operation"""
    logger.info(f"Operation: {operation}, Data: {kwargs}")

class ConfigLoader:
    """Load configuration"""

    @staticmethod
    def load_from_dict(data: Dict) -> Dict:
        """Load from dictionary"""
        return data

    @staticmethod
    def load_from_json(path: str) -> Dict:
        """Load from JSON file"""
        with open(path) as f:
            return json.load(f)

def retry(max_attempts: int = 3):
    """Decorator for retry logic"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt+1} failed: {e}")
        return wrapper
    return decorator
