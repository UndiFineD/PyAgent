# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\VolatilityThreshold_BT.py
# 🌙 Moon Dev's Volatility Threshold Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data 🌟
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class VolatilityThreshold(Strategy):
    risk_pct = 0.01  # 1% risk per trade 🌕
    atr_window = 20 * 96  # 20 days in 15m periods
    sma_period = 200 * 96  # 200-day SMA ✨
    hold_period = 5 * 96  # 5-day hold 🕒
    percentile_window = 252 * 96  # 1-year lookback 🌗

    def init(self):
        # 🌙 Core Indicators
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.atr_window,
            name="ATR_20",
        )
        self.sma = self.I(talib.SMA, self.data.Close, self.sma_period, name="SMA_200")

        # ✨ Dynamic ATR Percentile Calculation
        def calc_percentile(series):
            return series.rolling(self.percentile_window).quantile(0.10)

        self.atr_percentile = self.I(calc_percentile, self.atr, name="ATR_10%")

        # 🌌 Trade tracking variables
        self.entry_price = None
        self.entry_atr = None
        self.entry_bar = 0

    def next(self):
        price = self.data.Close[-1]

        # 🌙 Moon Dev Debug Prints
        if len(self.data) % 1000 == 0:
            print(
                f"🌙 Bar {len(self.data)} | Price: {price:.2f} | ATR: {self.atr[-1]:.2f} vs {self.atr_percentile[-1]:.2f}"
            )

        # 🚀 Entry Logic
        if not self.position:
            if self.atr[-1] < self.atr_percentile[-1] and price > self.sma[-1]:

                # 🌕 Risk Management Calculation
                sl = price - 2 * self.atr[-1]
                risk_amount = self.risk_pct * self.equity
                position_size = risk_amount / (price - sl)
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_price = price
                    self.entry_atr = self.atr[-1]
                    self.entry_bar = len(self.data)
                    print(
                        f"🚀 LONG ENTRY 🌕 | Size: {position_size} | Price: {price:.2f} | SL: {sl:.2f}"
                    )

        # 🔴 Exit Logic
        else:
            # Stop Loss Check
            current_low = self.data.Low[-1]
            sl_price = self.entry_price - 2 * self.entry_atr

            if current_low <= sl_price:
                self.position.close()
                print(
                    f"🔴 STOP LOSS EXIT | Price: {price:.2f} | Bars Held: {len(self.data)-self.entry_bar}"
                )

            # Time Exit Check
            elif len(self.data) - self.entry_bar >= self.hold_period:
                self.position.close()
                print(
                    f"🕒 TIME EXIT | Price: {price:.2f} | Bars Held: {len(self.data)-self.entry_bar}"
                )


# 🌟 Run Backtest
bt = Backtest(data, VolatilityThreshold, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🌙 Print Full Results
print("\n" + "=" * 50 + " MOON DEV FINAL STATS 🌙 " + "=" * 50)
print(stats)
print(stats._strategy)
print("🌙 Backtest Complete! May the Moon Phase Be With You! 🌕✨")
