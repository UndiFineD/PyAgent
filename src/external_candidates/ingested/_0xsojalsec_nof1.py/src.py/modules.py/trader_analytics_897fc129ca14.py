# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-nof1.ai-alpha-arena\src\modules\trader_analytics.py
"""
Identify top-performing traders on Polymarket.
Simulated.
"""


class TraderAnalytics:
    @staticmethod
    def get_top_traders():
        traders = [
            {"name": "TraderA", "win_rate": 0.82},
            {"name": "TraderB", "win_rate": 0.76},
            {"name": "TraderC", "win_rate": 0.91},
        ]
        return sorted(traders, key=lambda t: t["win_rate"], reverse=True)
