# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentBandReversion_AI7.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 AI7 - DivergentBandReversion Strategy Backtest
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


class DivergentBandReversion(Strategy):
    time_exit_bars = 10
    risk_percent = 0.02

    def init(self):
        # MACD Calculation
        def _macd_line(close):
            macd_df = ta.macd(pd.Series(close), fast=12, slow=26, signal=9)
            if macd_df is not None and len(macd_df.columns) > 0:
                return macd_df.iloc[:, 0].values  # MACD line
            else:
                # Fallback simple calculation
                ema_fast = pd.Series(close).ewm(span=12).mean()
                ema_slow = pd.Series(close).ewm(span=26).mean()
                return (ema_fast - ema_slow).values

        self.macd = self.I(_macd_line, self.data.Close, name="MACD")

        # Rolling max/min for swing points
        def _rolling_max(data, window):
            return pd.Series(data).rolling(window=window, center=True).max().values

        def _rolling_min(data, window):
            return pd.Series(data).rolling(window=window, center=True).min().values

        self.swing_high_price = self.I(
            _rolling_max, self.data.High, 5, name="Swing High"
        )
        self.swing_low_price = self.I(_rolling_min, self.data.Low, 5, name="Swing Low")
        self.swing_high_macd = self.I(
            _rolling_max, self.macd, 5, name="MACD Swing High"
        )
        self.swing_low_macd = self.I(_rolling_min, self.macd, 5, name="MACD Swing Low")

        # Bollinger Bands
        def _bbands_upper2(close):
            bb = ta.bbands(pd.Series(close), length=20, std=2)
            if bb is not None:
                return bb.iloc[:, 0].values  # upper
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma + 2 * std).values

        def _bbands_lower2(close):
            bb = ta.bbands(pd.Series(close), length=20, std=2)
            if bb is not None:
                return bb.iloc[:, 2].values  # lower
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma - 2 * std).values

        def _bbands_upper3(close):
            bb = ta.bbands(pd.Series(close), length=20, std=3)
            if bb is not None:
                return bb.iloc[:, 0].values  # upper
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma + 3 * std).values

        def _bbands_lower3(close):
            bb = ta.bbands(pd.Series(close), length=20, std=3)
            if bb is not None:
                return bb.iloc[:, 2].values  # lower
            else:
                sma = pd.Series(close).rolling(20).mean()
                std = pd.Series(close).rolling(20).std()
                return (sma - 3 * std).values

        self.upper2 = self.I(_bbands_upper2, self.data.Close, name="BB2σ Upper")
        self.lower2 = self.I(_bbands_lower2, self.data.Close, name="BB2σ Lower")
        self.upper3 = self.I(_bbands_upper3, self.data.Close, name="BB3σ Upper")
        self.lower3 = self.I(_bbands_lower3, self.data.Close, name="BB3σ Lower")

        # Simple Moving Average
        def _sma(close, period):
            result = ta.sma(pd.Series(close), length=period)
            if result is not None:
                return result.values
            else:
                return pd.Series(close).rolling(period).mean().values

        self.middle_band = self.I(_sma, self.data.Close, 20, name="SMA20")

        # ATR for volatility-based stops
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

        self.last_swing_high_price = None
        self.last_swing_high_macd = None
        self.last_swing_low_price = None
        self.last_swing_low_macd = None

    def next(self):
        # Skip if not enough data
        if len(self.data.Close) < 30:
            return

        # Update swing points and detect divergences
        bearish_div = False
        bullish_div = False

        # Check for new swing highs
        if (
            len(self.swing_high_price) > 1
            and self.data.High[-1] == self.swing_high_price[-1]
        ):
            if self.last_swing_high_price is not None:
                bearish_div = (
                    self.swing_high_price[-1] > self.last_swing_high_price
                ) and (self.swing_high_macd[-1] < self.last_swing_high_macd)
                if bearish_div:
                    print(
                        f"🌑 Bearish divergence detected! Price: {self.swing_high_price[-1]:.2f}, MACD: {self.swing_high_macd[-1]:.2f}"
                    )
            self.last_swing_high_price = self.swing_high_price[-1]
            self.last_swing_high_macd = self.swing_high_macd[-1]

        # Check for new swing lows
        if (
            len(self.swing_low_price) > 1
            and self.data.Low[-1] == self.swing_low_price[-1]
        ):
            if self.last_swing_low_price is not None:
                bullish_div = (
                    self.swing_low_price[-1] < self.last_swing_low_price
                ) and (self.swing_low_macd[-1] > self.last_swing_low_macd)
                if bullish_div:
                    print(
                        f"🚀 Bullish divergence detected! Price: {self.swing_low_price[-1]:.2f}, MACD: {self.swing_low_macd[-1]:.2f}"
                    )
            self.last_swing_low_price = self.swing_low_price[-1]
            self.last_swing_low_macd = self.swing_low_macd[-1]

        # Entry Logic
        if not self.position:
            current_price = self.data.Close[-1]

            # Long Entry: Bullish divergence + price near lower band + reversal signal
            if (
                bullish_div
                and current_price <= self.lower2[-1] * 1.02  # Near lower 2σ band
                and current_price > self.lower3[-1]  # Above extreme 3σ band
                and self.macd[-1] > self.macd[-2]
            ):  # MACD turning up

                # Calculate position sizing
                entry_price = current_price
                sl_price = self.lower3[-1] - (self.atr[-1] * 0.5)  # Stop below 3σ band
                tp_price = self.middle_band[-1]  # Target middle band

                # Ensure correct order: SL < entry < TP for long trades
                if sl_price >= entry_price:
                    sl_price = entry_price * 0.98  # 2% stop below entry

                if tp_price <= entry_price:
                    tp_price = entry_price * 1.02  # 2% target above entry

                risk_amount = self.equity * self.risk_percent
                risk_per_share = entry_price - sl_price

                if risk_per_share > 0 and sl_price < entry_price < tp_price:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🌙💚 LONG: Entry={entry_price:.2f} | SL={sl_price:.2f} | TP={tp_price:.2f} | Size={position_size}"
                        )

            # Short Entry: Bearish divergence + price near upper band + reversal signal
            elif (
                bearish_div
                and current_price >= self.upper2[-1] * 0.98  # Near upper 2σ band
                and current_price < self.upper3[-1]  # Below extreme 3σ band
                and self.macd[-1] < self.macd[-2]
            ):  # MACD turning down

                # Calculate position sizing
                entry_price = current_price
                sl_price = self.upper3[-1] + (self.atr[-1] * 0.5)  # Stop above 3σ band
                tp_price = self.middle_band[-1]  # Target middle band

                # Ensure correct order: TP < entry < SL for short trades
                if tp_price >= entry_price:
                    tp_price = entry_price * 0.98  # 2% target below entry

                if sl_price <= entry_price:
                    sl_price = entry_price * 1.02  # 2% stop above entry

                risk_amount = self.equity * self.risk_percent
                risk_per_share = sl_price - entry_price

                if risk_per_share > 0 and tp_price < entry_price < sl_price:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.sell(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🌙❤️ SHORT: Entry={entry_price:.2f} | SL={sl_price:.2f} | TP={tp_price:.2f} | Size={position_size}"
                        )

        # Time-based exit
        elif (
            self.position
            and (len(self.data) - self.position.entry_bar) >= self.time_exit_bars
        ):
            self.position.close()
            print(f"🌙⏰ TIME EXIT: Held {self.time_exit_bars} bars")


# 🌙🚀 Execute Backtest
print("🌙✨ Starting DivergentBandReversion Backtest...")
bt = Backtest(data, DivergentBandReversion, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌙🎯 BACKTEST RESULTS - DivergentBandReversion Strategy:")
print("=" * 60)
print(stats)
print("\n🌙📊 Strategy Details:")
print(stats._strategy)
print("=" * 60)
