# Extracted from: C:\DEV\PyAgent\.external\skills\skills\s7cret\binance-enhanced\monitoring\utils\data_loader.py
"""Small helpers to load sample data (for prototype/testing)"""

import json
from pathlib import Path

BASE = Path(__file__).parents[2]


def load_sample_portfolio():
    p = BASE / "sample_data" / "portfolio_sample.json"
    return json.loads(p.read_text())
