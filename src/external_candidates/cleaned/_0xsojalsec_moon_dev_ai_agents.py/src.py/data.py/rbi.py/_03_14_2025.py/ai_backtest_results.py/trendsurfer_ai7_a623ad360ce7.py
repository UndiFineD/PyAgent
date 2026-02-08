# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\TrendSurfer_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - TrendSurfer Strategy Backtest
Moon Dev AI Trading Strategy Implementation
Aggressive trend following to beat buy and hold
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


class TrendSurfer(Strategy):
    # More aggressive parameters
    ema_fast = 8
    ema_slow = 21
    lookback = 20
    breakout_threshold = 0.02  # 2% breakout required
    position_size_pct = 0.95  # Use 95% of equity per trade

    def init(self):
        # Exponential moving averages for faster trend detection
        def _ema_fast(close):
            result = ta.ema(pd.Series(close), length=self.ema_fast)
            if result is not None:
                return result.values
            else:
                return pd.Series(close).ewm(span=self.ema_fast).mean().values

        def _ema_slow(close):
            result = ta.ema(pd.Series(close), length=self.ema_slow)
            if result is not None:
                return result.values
            else:
                return pd.Series(close).ewm(span=self.ema_slow).mean().values

        self.ema_fast_line = self.I(_ema_fast, self.data.Close, name=f"EMA{self.ema_fast}")
        self.ema_slow_line = self.I(_ema_slow, self.data.Close, name=f"EMA{self.ema_slow}")

        # Rolling highs and lows for breakout detection
        def _rolling_high(high, period):
            return pd.Series(high).rolling(period).max().values

        def _rolling_low(low, period):
            return pd.Series(low).rolling(period).min().values

        self.highest = self.I(_rolling_high, self.data.High, self.lookback, name=f"High{self.lookback}")
        self.lowest = self.I(_rolling_low, self.data.Low, self.lookback, name=f"Low{self.lookback}")

        # ATR for dynamic position sizing
        def _atr(high, low, close, period=14):
            result = ta.atr(pd.Series(high), pd.Series(low), pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                tr = np.maximum(
                    pd.Series(high) - pd.Series(low),
                    np.maximum(
                        abs(pd.Series(high) - pd.Series(close).shift(1)),
                        abs(pd.Series(low) - pd.Series(close).shift(1)),
                    ),
                )
                return tr.rolling(period).mean().values

        self.atr = self.I(_atr, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # Skip if not enough data
        if len(self.data.Close) < max(self.ema_slow, self.lookback):
            return

        price = self.data.Close[-1]

        # Trend signals
        ema_bullish = self.ema_fast_line[-1] > self.ema_slow_line[-1]
        ema_bearish = self.ema_fast_line[-1] < self.ema_slow_line[-1]

        # Breakout signals
        breakout_high = price > self.highest[-1] * (1 + self.breakout_threshold)
        breakout_low = price < self.lowest[-1] * (1 - self.breakout_threshold)

        # Strong trend confirmation
        strong_uptrend = (
            price > self.ema_fast_line[-1] > self.ema_slow_line[-1] and self.ema_fast_line[-1] > self.ema_fast_line[-2]
        )
        strong_downtrend = (
            price < self.ema_fast_line[-1] < self.ema_slow_line[-1] and self.ema_fast_line[-1] < self.ema_fast_line[-2]
        )

        if not self.position:
            # LONG Entry: Strong uptrend + breakout
            if (strong_uptrend and breakout_high) or (ema_bullish and breakout_high):
                # Use most of equity for maximum gains
                position_value = self.equity * self.position_size_pct
                position_size = int(position_value / price)

                if position_size > 0:
                    # Loose stop loss to ride trends
                    sl_price = self.ema_slow_line[-1] * 0.92  # 8% below slow EMA

                    self.buy(size=position_size, sl=sl_price)
                    print(f"🚀🌊 LONG TREND: {price:.2f} | SL: {sl_price:.2f} | Size: {position_size}")

            # SHORT Entry: Strong downtrend + breakdown
            elif (strong_downtrend and breakout_low) or (ema_bearish and breakout_low):
                # Use most of equity for maximum gains
                position_value = self.equity * self.position_size_pct
                position_size = int(position_value / price)

                if position_size > 0:
                    # Loose stop loss to ride trends
                    sl_price = self.ema_slow_line[-1] * 1.08  # 8% above slow EMA

                    self.sell(size=position_size, sl=sl_price)
                    print(f"🐻🌊 SHORT TREND: {price:.2f} | SL: {sl_price:.2f} | Size: {position_size}")

        else:
            # Exit logic - trend reversal
            if self.position.is_long:
                # Exit long if EMA trend reverses or price drops below slow EMA
                if self.ema_fast_line[-1] < self.ema_slow_line[-1] or price < self.ema_slow_line[-1] * 0.95:
                    self.position.close()
                    print(f"🌊 EXIT LONG: {price:.2f}")

            elif self.position.is_short:
                # Exit short if EMA trend reverses or price rises above slow EMA
                if self.ema_fast_line[-1] > self.ema_slow_line[-1] or price > self.ema_slow_line[-1] * 1.05:
                    self.position.close()
                    print(f"🌊 EXIT SHORT: {price:.2f}")


# 🌙🚀 Execute Backtest
print("🌙✨ Starting TrendSurfer Backtest...")
bt = Backtest(data, TrendSurfer, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - TrendSurfer Strategy:")
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
