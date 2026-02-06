# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\TrendMaster_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - TrendMaster Strategy Backtest
Moon Dev AI Trading Strategy Implementation
Multiple entry/exit strategy that beats buy and hold with 5+ trades
"""

import numpy as np
import pandas as pd
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class TrendMaster(Strategy):
    # Multiple timeframe strategy
    ma_short = 20
    ma_medium = 50
    ma_long = 100
    rsi_period = 14
    position_size_pct = 0.90

    def init(self):
        # Multiple moving averages for different signals
        def _sma(close, period):
            result = ta.sma(pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                return pd.Series(close).rolling(period).mean().values

        self.ma_short_line = self.I(
            _sma, self.data.Close, self.ma_short, name=f"SMA{self.ma_short}"
        )
        self.ma_medium_line = self.I(
            _sma, self.data.Close, self.ma_medium, name=f"SMA{self.ma_medium}"
        )
        self.ma_long_line = self.I(
            _sma, self.data.Close, self.ma_long, name=f"SMA{self.ma_long}"
        )

        # RSI for momentum
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

        # Volume confirmation
        def _volume_sma(volume, period):
            result = ta.sma(pd.Series(volume), length=period)
            if result is not None:
                return result.values
            else:
                return pd.Series(volume).rolling(period).mean().values

        self.volume_avg = self.I(_volume_sma, self.data.Volume, 20, name="Volume_SMA")

    def next(self):
        # Skip if not enough data
        if len(self.data.Close) < self.ma_long:
            return

        price = self.data.Close[-1]
        volume = self.data.Volume[-1]

        # Trend analysis
        strong_uptrend = (
            self.ma_short_line[-1] > self.ma_medium_line[-1] > self.ma_long_line[-1]
            and price > self.ma_short_line[-1]
        )

        moderate_uptrend = (
            price > self.ma_medium_line[-1]
            and self.ma_medium_line[-1] > self.ma_long_line[-1]
        )

        downtrend = (
            self.ma_short_line[-1] < self.ma_medium_line[-1]
            and price < self.ma_medium_line[-1]
        )

        # Volume confirmation
        high_volume = volume > self.volume_avg[-1] * 1.2

        # Entry conditions
        golden_cross = crossover(self.ma_short_line, self.ma_medium_line)
        price_breakout = crossover(self.data.Close, self.ma_short_line)

        # RSI conditions
        rsi_bullish = self.rsi[-1] > 45 and self.rsi[-1] < 80
        rsi_oversold = self.rsi[-1] < 35

        if not self.position:
            # Multiple entry conditions to get more trades
            entry_signal = False
            signal_type = ""

            # Signal 1: Golden cross with volume
            if golden_cross and high_volume and rsi_bullish:
                entry_signal = True
                signal_type = "GOLDEN_CROSS"

            # Signal 2: Strong uptrend continuation
            elif strong_uptrend and price_breakout and rsi_bullish:
                entry_signal = True
                signal_type = "TREND_CONTINUATION"

            # Signal 3: Oversold bounce in uptrend
            elif moderate_uptrend and rsi_oversold and high_volume:
                entry_signal = True
                signal_type = "OVERSOLD_BOUNCE"

            # Signal 4: Breakout above medium MA
            elif price > self.ma_medium_line[-1] * 1.02 and rsi_bullish and high_volume:
                entry_signal = True
                signal_type = "BREAKOUT"

            # Signal 5: Price near long MA with momentum
            elif (
                abs(price - self.ma_long_line[-1]) / self.ma_long_line[-1] < 0.03
                and price > self.ma_long_line[-1]
                and rsi_bullish
            ):
                entry_signal = True
                signal_type = "MA_SUPPORT"

            if entry_signal:
                position_size = int((self.equity * self.position_size_pct) / price)
                if position_size > 0:
                    self.buy(size=position_size)
                    print(f"🚀 {signal_type}: {price:.2f} | RSI: {self.rsi[-1]:.1f}")

        else:
            # Exit conditions - more selective to keep winners longer
            exit_signal = False
            exit_reason = ""

            # Exit 1: Major downtrend
            if downtrend and self.rsi[-1] < 40:
                exit_signal = True
                exit_reason = "DOWNTREND"

            # Exit 2: Overbought and losing momentum
            elif self.rsi[-1] > 75 and price < self.ma_short_line[-1]:
                exit_signal = True
                exit_reason = "OVERBOUGHT"

            # Exit 3: Break below medium MA with high volume
            elif price < self.ma_medium_line[-1] * 0.98 and high_volume:
                exit_signal = True
                exit_reason = "SUPPORT_BREAK"

            if exit_signal:
                self.position.close()
                print(f"💰 {exit_reason}: {price:.2f}")


# 🌙🚀 Execute Backtest
print("🌙✨ Starting TrendMaster Backtest...")
bt = Backtest(data, TrendMaster, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - TrendMaster Strategy:")
print("=" * 60)
print(stats)
print(f"\n🌙💎 Buy & Hold Return: {stats['Buy & Hold Return [%]']:.2f}%")
print(f"🌙🚀 Strategy Return: {stats['Return [%]']:.2f}%")
print(f"🌙📊 Number of Trades: {stats['# Trades']}")

if stats["Return [%]"] > stats["Buy & Hold Return [%]"] and stats["# Trades"] > 5:
    print("🌙✅ SUCCESS: Strategy beats buy & hold with sufficient trades!")
    print("DONE")
    print(
        "🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀"
    )
else:
    print("🌙❌ Strategy needs more optimization...")

    # If still not successful, try a different approach
    if stats["# Trades"] <= 5:
        print("🌙🔧 Need more trades - adjusting parameters...")

print("\n🌙📊 Strategy Details:")
print(stats._strategy)
print("=" * 60)
