# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_01_2025\backtests_package\VolatilityImbalance_PKG.py
# 🌙 Moon Dev Backtest System - VolatilityImbalance Strategy 🚀
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🧹 Data Cleaning & Preparation 🌊
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Cleanse column names with Moon Dev Magic ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Cosmic Column Alignment 🌌
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Calculate Order Book Imbalance (🌓 Lunar Balance Metric)
data["imbalance_ratio"] = data["bidvolume"] / data["askvolume"]  # Assumes bid/ask volume columns exist


class VolatilityImbalance(Strategy):
    def init(self):
        # 🌗 Phase 1: Cosmic Indicators Setup
        # Using talib for Bollinger Bands
        upper, middle, lower = talib.BBANDS(self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        self.upper_band = self.I(lambda: upper, name="Upper Band")
        self.middle_band = self.I(lambda: middle, name="Middle Band")
        self.lower_band = self.I(lambda: lower, name="Lower Band")

        # 🌠 Bollinger Band Width Calculation
        self.bbw = self.I(lambda: (upper - lower) / middle, name="BB Width")
        self.bbw_sma = self.I(talib.SMA, self.bbw, timeperiod=20, name="BB Width SMA")

        # 📊 Order Book Imbalance Metrics
        self.imbalance_mean = self.I(
            talib.SMA,
            self.data.df["imbalance_ratio"],
            timeperiod=20,
            name="Imbalance Mean",
        )
        self.imbalance_std = self.I(
            talib.STDDEV,
            self.data.df["imbalance_ratio"],
            timeperiod=20,
            name="Imbalance STD",
        )

        # 🛡️ Risk Management Guardians
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )

        print("🌙 Lunar Systems Online - Trading Protocol Activated 🚀")

    def next(self):
        # 🕰️ Time Gate: Ensure enough historical data
        if len(self.data) < 20:
            return

        # 🌌 Current Cosmic Readings
        price = self.data.Close[-1]
        imb = self.data.df["imbalance_ratio"][-1]
        imb_z = (imb - self.imbalance_mean[-1]) / self.imbalance_std[-1]
        bbw = self.bbw[-1]
        bbw_ma = self.bbw_sma[-1]
        upper = self.upper_band[-1]

        # 🌕 Long Entry Constellation Alignment
        if not self.position:
            if imb_z > 2 and bbw < bbw_ma:
                # 🧮 Risk Calculation Ritual
                risk_amount = self.equity * 0.01  # 1% risk
                atr = self.atr[-1] or 1  # Prevent division by zero
                position_size = int(round(risk_amount / atr))

                # 🚀 Launch Position with Cosmic Safeguards
                self.buy(size=position_size, sl=self.lower_band[-1])
                print(f"🌙✨ CELESTIAL BUY SIGNAL ✨ {price:.2f}")
                print(f"📈 Size: {position_size} | 🛡️ SL: {self.lower_band[-1]:.2f}")

        # 🌑 Exit Protocol: Starlight Profit Capture
        else:
            if price >= upper:
                self.position.close()
                print(f"🚀🌗 STARLIGHT EXIT {price:.2f} | Profit: {self.position.pl:.2f}")


# 🌕 Moon Dev Backtest Launch Sequence
bt = Backtest(data, VolatilityImbalance, cash=1_000_000)
stats = bt.run()
print("\n🌙✨ FINAL MOON DEV STRATEGY STATS ✨🌙")
print(stats)
print(stats._strategy)
