# Extracted from: C:\DEV\PyAgent\.external\skills\skills\zbruceli\unifai-trading-suite\src\markets\__init__.py
"""Prediction market integrations."""

from .kalshi import KalshiClient
from .polymarket import PolymarketClient

__all__ = ["KalshiClient", "PolymarketClient"]
