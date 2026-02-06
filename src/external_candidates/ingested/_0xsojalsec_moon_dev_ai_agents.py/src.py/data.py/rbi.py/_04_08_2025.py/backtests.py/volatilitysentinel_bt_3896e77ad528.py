# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests\VolatilitySentinel_BT.py
# 🌙 Moon Dev's VolatilitySentinel Backtest Implementation 🚀

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Data Preparation 🌍
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns 🧹
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


class VolatilitySentinel(Strategy):
    risk_pct = 0.02  # 🌑 2% risk per trade
    ema_period = 3
    median_period = 21
    vol_lookback = 20  # For realized volatility

    def init(self):
        # Indicator Calculation 🌗
        put_call = self.data.df["put_call_ratio"]

        # Core Indicators
        self.ema_putcall = self.I(talib.EMA, put_call, self.ema_period, name="EMA3_PCR")
        self.median_putcall = self.I(
            lambda s: s.rolling(self.median_period).median(), put_call, name="MED21_PCR"
        )
        self.vix_spread = self.I(
            lambda: self.data.df["vix_near"] - self.data.df["vix_next"],
            name="VIX_SPREAD",
        )
        self.realized_vol = self.I(
            talib.STDDEV, self.data.Close, self.vol_lookback, name="REALIZED_VOL"
        )

        print("🌙✨ Volatility Sentinel Activated! Initial Indicators:")
        print(
            f"EMA({self.ema_period}) PCR | MED({self.median_period}) PCR | VIX Spread | {self.vol_lookback}-Period Vol"
        )

    def next(self):
        if self.position:
            return  # 🛑 Existing position management

        # Entry Conditions Check 🔍
        ema_cross = crossover(self.ema_putcall, self.median_putcall)
        vix_confirmation = self.vix_spread[-1] > 0  # Backwardation

        if ema_cross and vix_confirmation:
            # Risk Management Calculation 🔒
            equity = self.equity
            risk_amount = equity * self.risk_pct
            entry_price = self.data.Close[-1]
            atr = self.realized_vol[-1]

            # Dynamic Stop Calculation 📏
            stop_price = entry_price + 2 * atr
            risk_per_unit = stop_price - entry_price

            if risk_per_unit <= 0:
                print("⚠️ Invalid Risk/Unit - Trade Aborted")
                return

            position_size = int(round(risk_amount / risk_per_unit))

            if position_size <= 0:
                print("⚠️ Zero Size Calculated - Trade Skipped")
                return

            # Execute Short Entry 🩳
            print(f"🚀🌑 MOON DEV SHORT SIGNAL!")
            print(
                f"Entry: {entry_price:.2f} | Size: {position_size} | Vol Stop: {stop_price:.2f}"
            )
            self.sell(size=position_size, sl=stop_price, tag="VolatilityStop")


# Backtest Execution 🔁
bt = Backtest(
    data, VolatilitySentinel, cash=1_000_000, commission=0.002, exclusive_orders=True
)

stats = bt.run()
print("\n🌕🌕🌕 FINAL BACKTEST RESULTS 🌕🌕🌕")
print(stats)
print(stats._strategy)
