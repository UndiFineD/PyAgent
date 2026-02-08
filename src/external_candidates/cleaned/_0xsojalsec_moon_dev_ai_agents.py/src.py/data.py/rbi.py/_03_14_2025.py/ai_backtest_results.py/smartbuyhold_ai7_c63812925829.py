# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\SmartBuyHold_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - SmartBuyHold Strategy Backtest
Moon Dev AI Trading Strategy Implementation
Smart version of buy and hold that beats regular buy and hold
"""

import numpy as np
import pandas as pd
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class SmartBuyHold(Strategy):
    # Smart parameters for optimal buy and hold timing
    ma_long = 200  # Long-term trend
    rsi_period = 14
    dip_threshold = 0.05  # Buy the dips (5% drop)
    position_size_pct = 0.95  # Use most of capital

    def init(self):
        # Long-term moving average for overall trend
        def _sma(close, period):
            result = ta.sma(pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                return pd.Series(close).rolling(period).mean().values

        self.ma_long_line = self.I(_sma, self.data.Close, self.ma_long, name=f"SMA{self.ma_long}")

        # RSI for oversold conditions
        def _rsi(close, period):
            result = ta.rsi(pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                delta = pd.Series(close).diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                return (100 - (100 / (1 + rs))).values

        self.rsi = self.I(_rsi, self.data.Close, self.rsi_period, name="RSI")

        # Track highest price for dip detection
        def _rolling_max(close, period):
            return pd.Series(close).rolling(period).max().values

        self.highest_recent = self.I(_rolling_max, self.data.Close, 20, name="HighestRecent")

    def next(self):
        # Skip if not enough data
        if len(self.data.Close) < self.ma_long:
            return

        price = self.data.Close[-1]

        # Only consider long positions in an overall uptrend
        in_uptrend = price > self.ma_long_line[-1] * 0.95  # Allow some deviation

        # Detect dips - price has dropped significantly from recent high
        dip_detected = (
            price < self.highest_recent[-1] * (1 - self.dip_threshold) and self.rsi[-1] < 40
        )  # Oversold condition

        # Strong momentum condition
        strong_momentum = price > self.ma_long_line[-1] and self.rsi[-1] > 50

        if not self.position:
            # BUY conditions:
            # 1. In overall uptrend AND (buying a dip OR strong momentum)
            # 2. Buy the dip when oversold in uptrend
            # 3. Buy momentum when breaking above long-term MA
            if in_uptrend and (dip_detected or strong_momentum):
                position_size = int((self.equity * self.position_size_pct) / price)
                if position_size > 0:
                    self.buy(size=position_size)

                    if dip_detected:
                        print(
                            f"🚀📉 BUY DIP: {price:.2f} | MA200: {self.ma_long_line[-1]:.2f} | RSI: {self.rsi[-1]:.1f}"
                        )
                    else:
                        print(
                            f"🚀📈 BUY MOMENTUM: {price:.2f} | MA200: {self.ma_long_line[-1]:.2f} | RSI: {self.rsi[-1]:.1f}"
                        )

        else:
            # EXIT conditions - only exit on major trend reversal
            # Exit if price drops significantly below long-term MA for extended period
            major_downtrend = (
                price < self.ma_long_line[-1] * 0.90  # 10% below MA200
                and self.rsi[-1] < 30
            )  # Very oversold

            if major_downtrend:
                self.position.close()
                print(f"💰🔻 EXIT: {price:.2f} | MA200: {self.ma_long_line[-1]:.2f} | Major downtrend detected")


# 🌙🚀 Execute Backtest
print("🌙✨ Starting SmartBuyHold Backtest...")
bt = Backtest(data, SmartBuyHold, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - SmartBuyHold Strategy:")
print("=" * 60)
print(stats)
print(f"\n🌙💎 Buy & Hold Return: {stats['Buy & Hold Return [%]']:.2f}%")
print(f"🌙🚀 Strategy Return: {stats['Return [%]']:.2f}%")
print(f"🌙📊 Number of Trades: {stats['# Trades']}")

if stats["Return [%]"] > stats["Buy & Hold Return [%]"] and stats["# Trades"] > 5:
    print("🌙✅ SUCCESS: Strategy beats buy & hold with sufficient trades!")
    print("DONE")
    print("🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀")
else:
    print("🌙❌ Strategy needs more optimization...")

print("\n🌙📊 Strategy Details:")
print(stats._strategy)
print("=" * 60)
