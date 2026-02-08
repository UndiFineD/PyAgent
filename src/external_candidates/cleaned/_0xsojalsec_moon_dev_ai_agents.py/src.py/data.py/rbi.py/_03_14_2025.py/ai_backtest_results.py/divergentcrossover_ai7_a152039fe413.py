# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentCrossover_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - DivergentCrossover Strategy Backtest
Moon Dev AI Trading Strategy Implementation
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


class DivergentCrossover(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # RSI with pandas_ta fallback
        def _rsi(close, period):
            result = ta.rsi(pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                # Simple RSI calculation
                delta = pd.Series(close).diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                return (100 - (100 / (1 + rs))).values

        self.rsi = self.I(_rsi, self.data.Close, 14, name="RSI")

        # MACD with pandas_ta fallback
        def _macd_line(close):
            macd_df = ta.macd(pd.Series(close), fast=12, slow=26, signal=9)
            if macd_df is not None and len(macd_df.columns) > 0:
                return macd_df.iloc[:, 0].values  # MACD line
            else:
                ema_fast = pd.Series(close).ewm(span=12).mean()
                ema_slow = pd.Series(close).ewm(span=26).mean()
                return (ema_fast - ema_slow).values

        def _macd_signal(close):
            macd_df = ta.macd(pd.Series(close), fast=12, slow=26, signal=9)
            if macd_df is not None and len(macd_df.columns) > 1:
                return macd_df.iloc[:, 1].values  # Signal line
            else:
                macd_line = _macd_line(close)
                return pd.Series(macd_line).ewm(span=9).mean().values

        def _macd_hist(close):
            macd_df = ta.macd(pd.Series(close), fast=12, slow=26, signal=9)
            if macd_df is not None and len(macd_df.columns) > 2:
                return macd_df.iloc[:, 2].values  # Histogram
            else:
                macd_line = _macd_line(close)
                signal_line = _macd_signal(close)
                return macd_line - signal_line

        self.macd = self.I(_macd_line, self.data.Close, name="MACD")
        self.signal = self.I(_macd_signal, self.data.Close, name="MACD Signal")
        self.hist = self.I(_macd_hist, self.data.Close, name="MACD Histogram")

        # CCI with pandas_ta fallback
        def _cci(high, low, close, period):
            result = ta.cci(pd.Series(high), pd.Series(low), pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                # Simple CCI calculation
                tp = (pd.Series(high) + pd.Series(low) + pd.Series(close)) / 3
                sma = tp.rolling(period).mean()
                mean_dev = tp.rolling(period).apply(lambda x: np.abs(x - x.mean()).mean())
                return ((tp - sma) / (0.015 * mean_dev)).values

        self.cci = self.I(_cci, self.data.High, self.data.Low, self.data.Close, 20, name="CCI")

        # Rolling swing highs and lows for divergence detection
        def _rolling_max(data, window):
            return pd.Series(data).rolling(window=window, center=True).max().values

        def _rolling_min(data, window):
            return pd.Series(data).rolling(window=window, center=True).min().values

        self.swing_high = self.I(_rolling_max, self.data.High, 20, name="Swing High")
        self.swing_low = self.I(_rolling_min, self.data.Low, 20, name="Swing Low")

        # Initialize swing tracking lists
        self.swing_highs = []
        self.swing_lows = []

    def next(self):
        # Skip if not enough data
        if len(self.data.Close) < 30:
            return

        bullish_divergence = bearish_divergence = False

        # Detect divergences
        if len(self.swing_high) > 1 and len(self.swing_low) > 1:
            # Check for new swing highs
            if len(self.swing_high) > 1 and self.swing_high[-1] != self.swing_high[-2]:
                if not np.isnan(self.swing_high[-1]) and not np.isnan(self.rsi[-1]):
                    self.swing_highs.append({"price": self.swing_high[-1], "rsi": self.rsi[-1]})
                    if len(self.swing_highs) > 1:
                        prev = self.swing_highs[-2]
                        if self.swing_high[-1] > prev["price"] and self.rsi[-1] < prev["rsi"]:
                            bearish_divergence = True
                            print(
                                f"🌙 BEARISH DIVERGENCE! Price ↗ {self.swing_high[-1]:.2f} vs {prev['price']:.2f}, RSI ↘ {self.rsi[-1]:.2f} vs {prev['rsi']:.2f}"
                            )

            # Check for new swing lows
            if len(self.swing_low) > 1 and self.swing_low[-1] != self.swing_low[-2]:
                if not np.isnan(self.swing_low[-1]) and not np.isnan(self.rsi[-1]):
                    self.swing_lows.append({"price": self.swing_low[-1], "rsi": self.rsi[-1]})
                    if len(self.swing_lows) > 1:
                        prev = self.swing_lows[-2]
                        if self.swing_low[-1] < prev["price"] and self.rsi[-1] > prev["rsi"]:
                            bullish_divergence = True
                            print(
                                f"🌙 BULLISH DIVERGENCE! Price ↘ {self.swing_low[-1]:.2f} vs {prev['price']:.2f}, RSI ↗ {self.rsi[-1]:.2f} vs {prev['rsi']:.2f}"
                            )

        # Get indicator crossover signals
        macd_cross = crossover(self.macd, self.signal)
        macd_death = crossover(self.signal, self.macd)
        hist_dir = self.hist[-1] > self.hist[-2] if len(self.hist) > 1 else False

        if not self.position:
            # Bullish entry logic
            if bullish_divergence and macd_cross and self.hist[-1] > 0 and self.cci[-1] < 100:
                entry_price = self.data.Close[-1]
                sl_price = entry_price * 0.98  # 2% stop loss
                tp_price = entry_price * 1.04  # 4% take profit

                risk_amount = self.equity * self.risk_percent
                risk_per_share = entry_price - sl_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🚀🌕 BULLISH ENTRY | Size: {position_size} | SL: {sl_price:.2f} | TP: {tp_price:.2f} | RSI: {self.rsi[-1]:.2f} CCI: {self.cci[-1]:.2f}"
                        )

            # Bearish entry logic
            elif bearish_divergence and macd_death and self.hist[-1] < 0 and self.cci[-1] > -100:
                entry_price = self.data.Close[-1]
                sl_price = entry_price * 1.02  # 2% stop loss above
                tp_price = entry_price * 0.96  # 4% take profit below

                risk_amount = self.equity * self.risk_percent
                risk_per_share = sl_price - entry_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.sell(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🐻🌑 BEARISH ENTRY | Size: {position_size} | SL: {sl_price:.2f} | TP: {tp_price:.2f} | RSI: {self.rsi[-1]:.2f} CCI: {self.cci[-1]:.2f}"
                        )


# 🌙🚀 Execute Backtest
print("🌙✨ Starting DivergentCrossover Backtest...")
bt = Backtest(data, DivergentCrossover, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - DivergentCrossover Strategy:")
print("=" * 60)
print(stats)
print("\n🌙📊 Strategy Details:")
print(stats._strategy)
print("=" * 60)
