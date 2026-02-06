# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentBands_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - DivergentBands Strategy Backtest
Moon Dev AI Trading Strategy Implementation
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


class DivergentBands(Strategy):
    atr_multiplier = 2
    risk_percentage = 0.01
    max_bars_in_trade = 10

    def init(self):
        # Bollinger Bands with pandas_ta fallback
        def _bbands_upper(close):
            bb = ta.bbands(pd.Series(close), length=20, std=2)
            if bb is not None and len(bb.columns) > 0:
                return bb.iloc[:, 0].values  # upper
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma + 2 * std).values

        def _bbands_lower(close):
            bb = ta.bbands(pd.Series(close), length=20, std=2)
            if bb is not None and len(bb.columns) > 2:
                return bb.iloc[:, 2].values  # lower
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma - 2 * std).values

        self.upper_band = self.I(_bbands_upper, self.data.Close, name="BB Upper")
        self.lower_band = self.I(_bbands_lower, self.data.Close, name="BB Lower")

        # ATR for volatility-based exits
        def _atr(high, low, close, period):
            result = ta.atr(
                pd.Series(high), pd.Series(low), pd.Series(close), length=period
            )
            if result is not None:
                return result.values
            else:
                # Simple ATR calculation
                tr = np.maximum(
                    pd.Series(high) - pd.Series(low),
                    np.maximum(
                        abs(pd.Series(high) - pd.Series(close).shift(1)),
                        abs(pd.Series(low) - pd.Series(close).shift(1)),
                    ),
                )
                return tr.rolling(period).mean().values

        self.atr = self.I(_atr, self.data.High, self.data.Low, self.data.Close, 14)

        # Volume confirmation using SMA
        def _sma_volume(volume, period):
            result = ta.sma(pd.Series(volume), length=period)
            if result is not None:
                return result.values
            else:
                return pd.Series(volume).rolling(period).mean().values

        self.volume_sma = self.I(_sma_volume, self.data.Volume, 5)

    def next(self):
        # Avoid repainting and ensure indicator stability
        if len(self.data.Close) < 20 or len(self.volume_sma) < 5:
            return

        # Entry Logic Core
        if not self.position:
            # 1. Check Bollinger Band divergence (expanding bands)
            if len(self.upper_band) > 2 and len(self.lower_band) > 2:
                spread_increasing = (
                    self.upper_band[-1] - self.lower_band[-1]
                    > self.upper_band[-2] - self.lower_band[-2]
                    > self.upper_band[-3] - self.lower_band[-3]
                )

                # 2. Price near lower band (within 1%)
                price_near_lower = self.data.Close[-1] <= self.lower_band[-1] * 1.01

                # 3. Volume confirmation (current < SMA)
                volume_confirmation = self.data.Volume[-1] < self.volume_sma[-1]

                if spread_increasing and price_near_lower and volume_confirmation:
                    # Risk Management Calculations with fixed percentages
                    entry_price = self.data.Close[-1]
                    sl_price = entry_price * 0.98  # 2% stop loss
                    tp_price = entry_price * 1.04  # 4% take profit

                    risk_amount = self.equity * self.risk_percentage
                    risk_per_share = entry_price - sl_price

                    if risk_per_share > 0:
                        position_size = int(round(risk_amount / risk_per_share))
                        if position_size > 0:
                            self.buy(size=position_size, sl=sl_price, tp=tp_price)
                            print(
                                f"🌙✨ LONG ENTRY: {entry_price:.2f} | SL: {sl_price:.2f} | TP: {tp_price:.2f} | SIZE: {position_size} 🚀"
                            )
                        else:
                            print(f"🌙⚠️ Position size zero: {position_size}")
                    else:
                        print(f"🌙⚠️ Negative risk per share: {risk_per_share}")

        # Position management handled by SL/TP orders
        pass


# 🌙🚀 Execute Backtest
print("🌙✨ Starting DivergentBands Backtest...")
bt = Backtest(data, DivergentBands, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - DivergentBands Strategy:")
print("=" * 60)
print(stats)
print("\n🌙📊 Strategy Details:")
print(stats._strategy)
print("=" * 60)
