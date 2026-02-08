# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_17_2025\backtests\VolumetricBreakout_BT.py
# 🌙 MOON DEV BACKTESTING IMPLEMENTATION FOR VOLUMETRIC BREAKOUT STRATEGY 🚀

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# =======================
# DATA PREPARATION 🌌
# =======================
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean column names and drop unnamed columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Map columns to backtesting.py requirements
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

# Convert index to datetime
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


# =======================
# STRATEGY CLASS 🌙
# =======================
class VolumetricBreakout(Strategy):
    ema50_period = 50
    ema200_period = 200
    volume_sma_period = 20
    atr_period = 14
    risk_pct = 0.01  # 1% risk per trade
    atr_multiplier = 2  # 2x ATR trailing stop

    def init(self):
        # 🌙 CORE INDICATORS
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema50_period, name="EMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema200_period, name="EMA200")
        self.volume_sma = self.I(
            talib.SMA,
            self.data.Volume,
            timeperiod=self.volume_sma_period,
            name="Volume SMA",
        )
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
            name="ATR",
        )

    def next(self):
        # Wait for sufficient data ✨
        if len(self.data) < 200:
            return

        # 🌙 ENTRY LOGIC
        if not self.position:
            # EMA crossover confirmation
            ema_crossover = crossover(self.ema50, self.ema200)

            # Volume spike check
            volume_above_avg = self.data.Volume[-1] > self.volume_sma[-1]

            if ema_crossover and volume_above_avg:
                # 🌙 RISK MANAGEMENT CALCULATIONS
                current_atr = self.atr[-1]
                if current_atr <= 0:
                    return  # Avoid invalid calculations

                # Calculate position size based on 1% risk
                risk_amount = self.risk_pct * self.equity
                stop_distance = current_atr * self.atr_multiplier
                position_size = risk_amount / stop_distance
                position_size = int(round(position_size))

                if position_size > 0:
                    # 🌙 ENTRY EXECUTION
                    self.buy(size=position_size)
                    print(f"🌙✨ MOON DEV ENTRY: Long {position_size} units at {self.data.Close[-1]:.2f}!")
                    # Initialize trailing stop tracker
                    self.highest_high = self.data.High[-1]

        # 🛑 EXIT LOGIC
        else:
            # Update trailing stop level
            self.highest_high = max(self.highest_high, self.data.High[-1])
            current_stop = self.highest_high - (self.atr[-1] * self.atr_multiplier)

            # Check for stop breach
            if self.data.Low[-1] < current_stop:
                self.position.close()
                print(f"🌙🛑 MOON DEV EXIT: Trail stop triggered at {current_stop:.2f}!")


# =======================
# BACKTEST EXECUTION 🚀
# =======================
bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌙 FINAL RESULTS
print("\n" + "=" * 40)
print("MOON DEV FINAL BACKTEST REPORT 🌕✨")
print("=" * 40)
print(stats)
print(stats._strategy)
