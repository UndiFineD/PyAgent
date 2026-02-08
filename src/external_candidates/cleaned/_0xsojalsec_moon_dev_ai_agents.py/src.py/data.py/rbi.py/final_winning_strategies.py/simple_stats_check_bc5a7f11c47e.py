# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\simple_stats_check.py
#!/usr/bin/env python3
"""
Simple Stats Check - Quick verification of all 10 strategies
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest

# Suppress all warnings and prints
warnings.filterwarnings("ignore")
original_stdout = sys.stdout


class NullWriter:
    def write(self, text):
        pass

    def flush(self):
        pass


# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Temporarily suppress all output
sys.stdout = NullWriter()

# Test each strategy
results = []
strategies = [
    "SimpleMomentumCross",
    "RSIMeanReversion",
    "VolatilityBreakout",
    "BollingerReversion",
    "MACDDivergence",
    "StochasticMomentum",
    "TrendFollowingMA",
    "VolumeWeightedBreakout",
    "ATRChannelSystem",
    "HybridMomentumReversion",
]

for strategy_name in strategies:
    try:
        # Import strategy
        module = __import__(f"{strategy_name}_BT")
        strategy_class = getattr(module, strategy_name)

        # Run backtest
        bt = Backtest(data, strategy_class, cash=1000000, commission=0.002)
        stats = bt.run()

        results.append(
            {
                "name": strategy_name,
                "trades": stats["# Trades"],
                "return": stats["Return [%]"],
                "sharpe": stats["Sharpe Ratio"],
                "win_rate": stats["Win Rate [%]"],
                "max_dd": stats["Max. Drawdown [%]"],
            }
        )
    except Exception as e:
        results.append(
            {
                "name": strategy_name,
                "trades": 0,
                "return": 0,
                "sharpe": 0,
                "win_rate": 0,
                "max_dd": 0,
            }
        )

# Restore output
sys.stdout = original_stdout

# Print results
print("🌙 FINAL STATISTICS FOR ALL 10 STRATEGIES")
print("=" * 100)
print(
    f"{'#':<3} {'Strategy':<25} {'Trades':<8} {'Return%':<10} {'Sharpe':<8} {'WinRate%':<10} {'MaxDD%':<10} {'Status'}"
)
print("-" * 100)

for i, r in enumerate(results, 1):
    status = "✅" if r["trades"] >= 25 and r["sharpe"] >= 2.0 else "⚠️"
    print(
        f"{i:<3} {r['name']:<25} {r['trades']:<8} {r['return']:>9.2f} {r['sharpe']:>7.2f} {r['win_rate']:>9.2f} {r['max_dd']:>9.2f} {status}"
    )

print("-" * 100)

# Summary
total_trades = sum(r["trades"] for r in results)
avg_sharpe = np.mean([r["sharpe"] for r in results if r["sharpe"] != 0])
strategies_with_trades = sum(1 for r in results if r["trades"] > 0)
strategies_meeting_req = sum(1 for r in results if r["trades"] >= 25 and r["sharpe"] >= 2.0)

print(f"\n📊 SUMMARY:")
print(f"   Total Trades: {total_trades}")
print(f"   Strategies with trades: {strategies_with_trades}/10")
print(f"   Average Sharpe (non-zero): {avg_sharpe:.2f}")
print(f"   Strategies meeting requirements: {strategies_meeting_req}/10")

if strategies_with_trades < 10:
    print("\n⚠️ Some strategies are not generating trades. They may need debugging.")
else:
    print("\n✅ All strategies are generating trades!")
