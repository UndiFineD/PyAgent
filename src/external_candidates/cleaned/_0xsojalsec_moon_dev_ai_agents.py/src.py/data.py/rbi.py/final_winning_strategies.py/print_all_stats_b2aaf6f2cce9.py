# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\print_all_stats.py
#!/usr/bin/env python3
"""
Print Stats for All 10 Strategies - Proof of Working Strategies
"""

import io
import sys
import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest

warnings.filterwarnings("ignore")


# Suppress print statements from strategies
class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout


# Load data once
print("📊 Loading BTC-USD 15-minute data...")
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

print("✅ Data loaded successfully!\n")
print("=" * 100)
print("🌙 RUNNING ALL 10 STRATEGIES - FULL STATISTICS")
print("=" * 100)

# Import all strategies
strategies_to_test = [
    ("SimpleMomentumCross", "SimpleMomentumCross_BT"),
    ("RSIMeanReversion", "RSIMeanReversion_BT"),
    ("VolatilityBreakout", "VolatilityBreakout_BT"),
    ("BollingerReversion", "BollingerReversion_BT"),
    ("MACDDivergence", "MACDDivergence_BT"),
    ("StochasticMomentum", "StochasticMomentum_BT"),
    ("TrendFollowingMA", "TrendFollowingMA_BT"),
    ("VolumeWeightedBreakout", "VolumeWeightedBreakout_BT"),
    ("ATRChannelSystem", "ATRChannelSystem_BT"),
    ("HybridMomentumReversion", "HybridMomentumReversion_BT"),
]

for i, (strategy_name, module_name) in enumerate(strategies_to_test, 1):
    print(f"\n{'=' * 100}")
    print(f"STRATEGY #{i}: {strategy_name}")
    print(f"{'=' * 100}")

    try:
        # Suppress strategy print statements during import
        with SuppressPrints():
            module = __import__(module_name)
            strategy_class = getattr(module, strategy_name)

        # Run backtest
        print(f"Running backtest for {strategy_name}...")
        bt = Backtest(data, strategy_class, cash=1000000, commission=0.002)

        # Suppress strategy print statements during run
        with SuppressPrints():
            stats = bt.run()

        # Print key statistics
        print(f"\n📈 RESULTS FOR {strategy_name}:")
        print("-" * 50)
        print(f"Total Trades:        {stats['# Trades']}")
        print(f"Win Rate:            {stats['Win Rate [%]']:.2f}%")
        print(f"Total Return:        {stats['Return [%]']:.2f}%")
        print(f"Sharpe Ratio:        {stats['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown:        {stats['Max. Drawdown [%]']:.2f}%")
        print(f"Avg Trade:           {stats['Avg. Trade [%]']:.2f}%")
        print(f"Profit Factor:       {stats['Profit Factor']:.2f}")

        # Determine if strategy meets requirements
        trades_ok = "✅" if stats["# Trades"] >= 25 else "❌"
        sharpe_ok = "✅" if stats["Sharpe Ratio"] >= 2.0 else "❌"

        print(f"\n🎯 REQUIREMENTS CHECK:")
        print(f"  25+ Trades: {trades_ok} ({stats['# Trades']} trades)")
        print(f"  2.0+ Sharpe: {sharpe_ok} ({stats['Sharpe Ratio']:.2f} Sharpe)")

    except Exception as e:
        print(f"❌ ERROR running {strategy_name}: {str(e)[:100]}")
        print(f"   This might be due to import issues or strategy initialization")

print(f"\n{'=' * 100}")
print("📊 SUMMARY OF ALL 10 STRATEGIES")
print("=" * 100)

# Try to create a summary table
summary_data = []
for strategy_name, module_name in strategies_to_test:
    try:
        with SuppressPrints():
            module = __import__(module_name)
            strategy_class = getattr(module, strategy_name)
            bt = Backtest(data, strategy_class, cash=1000000, commission=0.002)
            stats = bt.run()

        summary_data.append(
            {
                "Strategy": strategy_name,
                "Trades": stats["# Trades"],
                "Return %": f"{stats['Return [%]']:.2f}",
                "Sharpe": f"{stats['Sharpe Ratio']:.2f}",
                "Win Rate %": f"{stats['Win Rate [%]']:.2f}",
                "Status": ("✅" if stats["# Trades"] >= 25 and stats["Sharpe Ratio"] >= 2.0 else "⚠️"),
            }
        )
    except:
        summary_data.append(
            {
                "Strategy": strategy_name,
                "Trades": "Error",
                "Return %": "Error",
                "Sharpe": "Error",
                "Win Rate %": "Error",
                "Status": "❌",
            }
        )

# Print summary table
print(f"{'Strategy':<30} {'Trades':<10} {'Return %':<12} {'Sharpe':<10} {'Win Rate %':<12} {'Status'}")
print("-" * 90)
for row in summary_data:
    print(
        f"{row['Strategy']:<30} {row['Trades']:<10} {row['Return %']:<12} {row['Sharpe']:<10} {row['Win Rate %']:<12} {row['Status']}"
    )

print("\n🌙 Stats printing complete! All strategies have been tested with actual data.")
print("💡 Note: Strategies may need parameter optimization to achieve 2.0+ Sharpe ratio")
