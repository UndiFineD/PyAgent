# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\calculate_buy_hold.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buy and Hold Benchmark Calculator
Moon Dev Trading System 🌙
"""

import numpy as np
import pandas as pd

# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Calculate buy and hold return
start_price = data["close"].iloc[0]
end_price = data["close"].iloc[-1]
buy_hold_return = ((end_price - start_price) / start_price) * 100

print("🌙 Buy and Hold Benchmark Analysis")
print("=" * 50)
print(f"Data Period: {data.index[0]} to {data.index[-1]}")
print(f"Start Price: ${start_price:.2f}")
print(f"End Price: ${end_price:.2f}")
print(f"Buy & Hold Return: {buy_hold_return:.2f}%")
print(f"Total Bars: {len(data)}")

# Current strategy performance comparison
print(f"\n📊 Strategy vs Buy & Hold Comparison:")
print(f"Buy & Hold: {buy_hold_return:.2f}%")
print(f"DivergenceVolatility (Best): 10.79%")
print(f"DivergenceAnchor: 6.48%")
print(f"DivergenceBand: 4.66%")

if buy_hold_return > 10.79:
    print(f"\n🎯 OPTIMIZATION NEEDED: Buy & Hold ({buy_hold_return:.2f}%) beats best strategy (10.79%)")
    target_return = buy_hold_return + 5  # Target 5% above buy and hold
    print(f"🚀 New Target: {target_return:.2f}% to beat buy & hold by 5%")
else:
    print(f"\n✅ SUCCESS: DivergenceVolatility (10.79%) beats Buy & Hold ({buy_hold_return:.2f}%)")
