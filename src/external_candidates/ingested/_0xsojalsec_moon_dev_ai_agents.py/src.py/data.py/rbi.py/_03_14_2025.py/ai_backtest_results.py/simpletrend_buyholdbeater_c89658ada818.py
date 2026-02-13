# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\SimpleTrend_BuyHoldBeater.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Trend Buy & Hold Beater Strategy
AI6 Implementation for Moon Dev Trading System 🌙
Target: Beat 127.77% buy & hold return with 5+ trades
"""

import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

warnings.filterwarnings("ignore")

# Load and prepare data
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


class SimpleTrendBuyHoldBeater(Strategy):
    """
    Simple Trend Following Strategy to Beat Buy & Hold

    Strategy: Buy on strong uptrend, hold until trend reverses
    Target: Beat 127.77% with minimal trades
    """

    # Simple parameters
    fast_ma = 20
    slow_ma = 50
    risk_per_trade = 0.8  # 80% of equity per trade (very aggressive)

    def init(self):
        # Simple moving averages
        def calc_sma(data, period):
            return pd.Series(data).rolling(window=period).mean().values

        self.fast_sma = self.I(calc_sma, self.data.Close, self.fast_ma)
        self.slow_sma = self.I(calc_sma, self.data.Close, self.slow_ma)

        # Track position
        self.entry_price = None
        self.total_trades = 0

    def next(self):
        if len(self.data) < max(self.fast_ma, self.slow_ma) + 1:
            return

        # Exit first
        if self.position:
            self.check_exits()
            return

        # Entry logic - golden cross + momentum
        if (
            self.fast_sma[-1] > self.slow_sma[-1]  # Golden cross
            and self.fast_sma[-2] <= self.slow_sma[-2]  # Just crossed
            and self.data.Close[-1] > self.fast_sma[-1]
        ):  # Price above fast MA

            self.execute_entry()

    def execute_entry(self):
        """Simple aggressive entry"""
        # Use most of available cash
        available_cash = self.equity * self.risk_per_trade
        position_size = int(available_cash / self.data.Close[-1])

        if position_size > 0:
            self.entry_price = self.data.Close[-1]
            self.total_trades += 1

            self.buy(size=position_size)

            print(
                f"🚀 TREND ENTRY #{self.total_trades}: Size={position_size} @ {self.entry_price:.2f}"
            )
            print(
                f"   Fast MA: {self.fast_sma[-1]:.2f} | Slow MA: {self.slow_sma[-1]:.2f}"
            )
            print(f"   Cash Used: ${available_cash:.0f}")

    def check_exits(self):
        """Exit on trend reversal or profit target"""
        current_price = self.data.Close[-1]

        # Exit on death cross
        if (
            self.fast_sma[-1] < self.slow_sma[-1]
            and self.fast_sma[-2] >= self.slow_sma[-2]
        ):
            self.position.close()
            profit = ((current_price - self.entry_price) / self.entry_price) * 100
            print(f"💀 DEATH CROSS EXIT @ {current_price:.2f} | Profit: {profit:.1f}%")
            self.entry_price = None
            return

        # Exit if price falls below slow MA
        if current_price < self.slow_sma[-1] * 0.98:
            self.position.close()
            profit = ((current_price - self.entry_price) / self.entry_price) * 100
            print(f"📉 TREND BREAK EXIT @ {current_price:.2f} | Profit: {profit:.1f}%")
            self.entry_price = None
            return


# Run backtest
print("🌙 Starting Simple Trend Buy & Hold Beater...")
print("Target: Beat 127.77% Buy & Hold Return")
print("=" * 50)

bt = Backtest(data, SimpleTrendBuyHoldBeater, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 Simple Trend Strategy Results:")
print("=" * 50)
print(stats)

# Key metrics
print(f"\n⭐ Performance Metrics:")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"🎯 Buy & Hold Benchmark: 127.77%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"📊 Total Trades: {stats['# Trades']}")

# Success check
if stats["Return [%]"] > 127.77 and stats["# Trades"] >= 5:
    print(f"\n🏆 SUCCESS! Strategy beats buy & hold!")
    print(f"   Strategy: {stats['Return [%]']:.2f}% vs Buy & Hold: 127.77%")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")
    print(f"   Outperformance: {stats['Return [%]'] - 127.77:.2f}%")
elif stats["# Trades"] >= 5:
    print(f"\n✅ TRADE COUNT MET but return insufficient")
    print(f"   Strategy: {stats['Return [%]']:.2f}% vs Buy & Hold: 127.77%")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")
    print(f"   Underperformance: {stats['Return [%]'] - 127.77:.2f}%")
else:
    print(f"\n❌ Requirements not met")
    print(f"   Return: {stats['Return [%]']:.2f}% (Target: >127.77%)")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")

print("\n🌙 Trend strategy completed! ✨")
