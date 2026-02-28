# Extracted from: C:\DEV\PyAgent\.external\skills\skills\adamkristopher\seo-dataforseo\scripts\core\__init__.py
"""Core module with client and storage utilities."""

from .client import get_client
from .storage import list_results, load_result, save_result

__all__ = ["get_client", "save_result", "load_result", "list_results"]
