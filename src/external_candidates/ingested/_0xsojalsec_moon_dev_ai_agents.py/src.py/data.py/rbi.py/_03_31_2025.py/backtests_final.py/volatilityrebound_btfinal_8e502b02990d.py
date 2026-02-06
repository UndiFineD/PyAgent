# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_31_2025\backtests_final\VolatilityRebound_BTFinal.py
# 🌙 Moon Dev's Volatility Rebound Backtest 🌙
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class VolatilityRebound(Strategy):
    timeperiod_bb = 20
    bb_dev = 2
    vol_lookback = 2880  # 30 days in 15m intervals
    exit_period = 48  # 12 hours in 15m intervals
    risk_percent = 0.01

    def init(self):
        # 🌙 Calculate Indicators with TA-Lib
        # Bollinger Bands
        self.lower_bb = self.I(
            lambda close: talib.BBANDS(
                close, self.timeperiod_bb, self.bb_dev, self.bb_dev, matype=0
            )[2],
            self.data.Close,
            name="LowerBB",
        )

        # Volume Percentile (90th)
        def vol_pct(volume):
            return volume.rolling(self.vol_lookback).quantile(0.9)

        self.vol_pct = self.I(vol_pct, self.data.Volume, name="VolumePct90")

        # Volatility Exit System
        upper_bb = self.I(
            lambda close: talib.BBANDS(
                close, self.timeperiod_bb, self.bb_dev, self.bb_dev, matype=0
            )[0],
            self.data.Close,
        )
        self.bb_width = self.I(
            lambda u, l: u - l, upper_bb, self.lower_bb, name="BBWidth"
        )
        self.bb_width_avg = self.I(
            lambda x: talib.SMA(x, self.exit_period), self.bb_width, name="BBWidthAvg"
        )

        print("✨ Moon Dev Indicators Initialized! ✨")

    def next(self):
        if not self.position:
            # 🌙 Entry Conditions Check
            if (
                self.data.fundingrate[-1] < 0
                and self.data.Volume[-1] > self.vol_pct[-1]
                and self.data.Low[-1] <= self.lower_bb[-1]
            ):

                # 🚀 Calculate Risk Management
                entry_price = self.data.Close[-1]
                bb_width = self.bb_width[-1]
                stop_loss = entry_price - 1.5 * bb_width
                risk_amount = self.equity * self.risk_percent
                risk_per_unit = abs(entry_price - stop_loss)

                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss)
                        print(
                            f"🚀 MOON DEV LONG ENTRY 🚀 | Price: {entry_price:.2f} | Size: {position_size} | SL: {stop_loss:.2f}"
                        )
        else:
            # 🌑 Exit Condition Check
            if self.bb_width[-1] < self.bb_width_avg[-1]:
                self.position.close()
                print(
                    f"🌑 VOLATILITY CONTRACTION EXIT 🌑 | Price: {self.data.Close[-1]:.2f}"
                )


# 🌙 Data Preparation Magic
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# 🪄 Ensure Proper Column Mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# 🌙 Add Funding Rate Check (assuming column exists as 'fundingrate')
assert (
    "fundingrate" in data.columns
), "❌ Missing funding rate column - Moon Dev data validation failed"

# 🚀 Launch Backtest
bt = Backtest(data, VolatilityRebound, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Print Moon Dev Performance Report
print("\n" + "=" * 50)
print("🌙 MOON DEV BACKTEST RESULTS 🌙")
print("=" * 50 + "\n")
print(stats)
print("\n" + "=" * 50)
print("STRATEGY PERFORMANCE BREAKDOWN")
print("=" * 50)
print(stats._strategy)
