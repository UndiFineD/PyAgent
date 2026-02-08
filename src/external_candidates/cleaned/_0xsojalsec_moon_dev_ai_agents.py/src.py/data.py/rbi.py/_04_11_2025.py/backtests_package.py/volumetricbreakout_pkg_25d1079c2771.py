# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_11_2025\backtests_package\VolumetricBreakout_PKG.py
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolumetricBreakout(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(columns=[col for col in self.data.df.columns if "unnamed" in col])

        # Calculate indicators using TA-Lib through self.I()
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.volume_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        print("✨ MOON INDICATORS INITIALIZED: BBANDS, SMA(20), RSI(14), ATR(14) ✨")

    def next(self):
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]
        price = self.data.Close[-1]

        # Entry Conditions 🌙🚀
        if not self.position and current_close > self.upper[-1] and current_volume > 2 * self.volume_ma[-1]:
            # Risk management calculations
            atr_value = self.atr[-1]
            stop_loss_price = price - 2 * atr_value
            risk_amount = self.risk_per_trade * self.equity
            risk_per_unit = price - stop_loss_price

            position_size = int(round(risk_amount / risk_per_unit))
            position_size = min(position_size, int(self.equity // price))  # Never exceed available equity

            print(f"🌙 MOON SIGNAL: BUY TRIGGERED! Size: {position_size} @ {price:.2f}")
            print(f"🚀 RISK MANAGEMENT: SL={stop_loss_price:.2f}, RSI={self.rsi[-1]:.2f}")

            self.buy(size=position_size, sl=stop_loss_price)

        # Exit Conditions 🌙💤
        if self.position:
            # Replaced crossover with direct comparison
            if self.rsi[-2] > 70 and self.rsi[-1] <= 70:
                print(f"💤 MOON EXIT: RSI CROSS BELOW 70 @ {self.data.Close[-1]:.2f}")
                self.position.close()


# Data preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"])
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
).set_index("datetime")

print("🌕 MOON DATA LOADED:")
print(f"📅 Date Range: {data.index[0]} to {data.index[-1]}")
print(f"📊 Columns: {data.columns.tolist()}")

# Run backtest
bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙✨ MOON DEV BACKTEST COMPLETE! FULL STATS BELOW ✨🌙")
print(stats)
print(stats._strategy)
