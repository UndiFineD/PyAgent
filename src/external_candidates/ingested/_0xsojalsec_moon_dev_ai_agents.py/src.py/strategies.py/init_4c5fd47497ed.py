# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\strategies\__init__.py
"""
🌙 Moon Dev's Strategies Package
"""

from .base_strategy import BaseStrategy

# We only need to export BaseStrategy - custom strategies will be loaded dynamically
__all__ = ["BaseStrategy"]
