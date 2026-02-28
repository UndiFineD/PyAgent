# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentPulse_AI8.py
#!/usr/bin/env python3
# 🌙 AI8 - DivergentPulse Strategy Implementation
# Moon Dev Trading Command Center

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data with lunar precision 🌕
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean data columns with cosmic care ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Rename columns to match backtesting requirements
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

# Convert datetime and set index with lunar alignment 🌑
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

print(f"🌙 Data loaded: {len(data)} rows from {data.index[0]} to {data.index[-1]}")


class DivergentPulse(Strategy):
    risk_pct = 0.01
    atr_period = 14
    swing_window = 5

    def init(self):
        print("🌙 Initializing DivergentPulse strategy with cosmic precision...")

        # Calculate core indicators 🌙
        self.macd, self.macd_signal, _ = self.I(
            talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )

        # Swing detection indicators ✨
        self.price_highs = self.I(
            talib.MAX, self.data.High, timeperiod=self.swing_window
        )
        self.price_lows = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_window)

        # Track trade date 🗓️
        self.last_trade_date = None

        print("✨ All cosmic indicators initialized successfully!")

    def next(self):
        # Skip early data
        if len(self.data) < 50:
            return

        # Removed daily trade limit to allow more trading opportunities

        # Simple divergence strategy based on RSI and MACD
        current_rsi = self.rsi[-1]
        current_macd = self.macd[-1]
        prev_rsi = self.rsi[-2] if len(self.rsi) > 1 else current_rsi
        prev_macd = self.macd[-2] if len(self.macd) > 1 else current_macd

        # Entry conditions - Made much more aggressive
        if not self.position:
            # Simple MACD crossover with RSI confirmation
            if (
                len(self.macd) > 1
                and len(self.macd_signal) > 1
                and self.macd[-1] > self.macd_signal[-1]  # MACD above signal
                and current_rsi < 60
            ):  # RSI not too overbought

                entry_price = self.data.Close[-1]
                atr_value = self.atr[-1] if len(self.atr) > 0 else entry_price * 0.02

                stop_loss = entry_price * 0.98  # Simple 2% stop
                risk_per_share = entry_price - stop_loss

                if risk_per_share > 0:
                    position_size = (self.equity * self.risk_pct) / risk_per_share
                    position_size = int(round(position_size))

                    if position_size > 0:
                        print(
                            f"🚀🌙 MACD Signal! Long {position_size} @ {entry_price:.2f}, SL: {stop_loss:.2f}"
                        )
                        self.buy(size=position_size, sl=stop_loss)
        # Exit conditions - Simple profit/loss targets
        else:
            entry_price = (
                self.position.entry_price
                if hasattr(self.position, "entry_price")
                else self.data.Close[-1]
            )
            current_price = self.data.Close[-1]

            # Exit on profit target, stop loss, or MACD bearish crossover
            if (
                current_price > entry_price * 1.03  # 3% profit
                or current_price < entry_price * 0.98  # 2% loss
                or (
                    len(self.macd) > 1
                    and len(self.macd_signal) > 1
                    and self.macd[-1] < self.macd_signal[-1]
                )
            ):  # MACD bearish crossover
                print(f"🚀🌑 Exit! Closing at {current_price:.2f}")
                self.position.close()


if __name__ == "__main__":
    print("🌙🚀 Starting DivergentPulse Backtest...")

    # Run backtest with lunar power 🌕
    bt = Backtest(data, DivergentPulse, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print full statistics with cosmic flair ✨
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔 DIVERGENT PULSE STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print("\n🌙 Strategy Details:")
    print(stats._strategy)

    print("\n🌙 DivergentPulse Backtest Complete! 🚀")
