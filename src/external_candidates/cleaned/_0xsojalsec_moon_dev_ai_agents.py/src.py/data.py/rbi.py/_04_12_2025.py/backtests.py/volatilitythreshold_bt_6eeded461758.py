# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_12_2025\backtests\VolatilityThreshold_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Moon Dev data preparation 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean and prepare data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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


class VolatilityThreshold(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌕

    def init(self):
        # Calculate indicators using TA-Lib 🌙
        self.atr_window = 20 * 24 * 4  # 20 days in 15m periods
        self.sma_window = 50 * 24 * 4  # 50 days in 15m periods

        # Core indicators ✨
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_window)
        self.sma50 = self.I(talib.SMA, self.data.Close, self.sma_window)

        # Historical ATR percentile calculation 🌌
        self.atr_percentile = self.I(lambda s: s.expanding().quantile(0.10), self.atr)

    def next(self):
        # Wait for indicators to warm up 🕒
        if len(self.data) < self.sma_window or pd.isna(self.atr[-1]) or pd.isna(self.atr_percentile[-1]):
            return

        current_close = self.data.Close[-1]
        current_atr = self.atr[-1]
        atr_threshold = self.atr_percentile[-1]
        sma_value = self.sma50[-1]

        # Moon Dev entry logic 🌙🚀
        if not self.position:
            if current_close > sma_value and current_atr < atr_threshold:
                # Risk management calculations 🔒
                risk_amount = self.equity * self.risk_percent
                stop_distance = 2 * current_atr
                position_size = risk_amount / stop_distance
                position_size = int(round(position_size))

                if position_size > 0:
                    print(f"🌕✨ MOON SHOT! Entry at {self.data.Open[-1]:.2f}")
                    print(f"   ATR({self.atr_window}): {current_atr:.2f} < Percentile: {atr_threshold:.2f}")
                    self.buy(size=position_size)

        # Exit logic 🌘
        else:
            position = self.position
            entry_price = position.entry_price
            bars_held = len(self.data) - position.entry_bar - 1

            # Dynamic stop loss 🛑
            stop_price = entry_price - (2 * self.atr[-1])
            if self.data.Low[-1] < stop_price:
                print(f"🔴🌒 STOPPED OUT! Loss: {position.pl_pct:.2%}")
                self.position.close()

            # Time-based exit ⏳
            elif bars_held >= 5 * 24 * 4:  # 5 days in 15m periods
                print(f"⏰🌓 TIME EXIT! Held {bars_held} bars")
                self.position.close()


# Launch backtest 🚀🌙
bt = Backtest(data, VolatilityThreshold, cash=1_000_000, trade_on_close=False)
stats = bt.run()
print(stats)
print(stats._strategy)
