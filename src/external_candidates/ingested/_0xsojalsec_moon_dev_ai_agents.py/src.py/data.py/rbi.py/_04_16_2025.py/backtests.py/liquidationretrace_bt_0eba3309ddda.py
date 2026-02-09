# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_16_2025\backtests\LiquidationRetrace_BT.py
# 🌙 MOON DEV BACKTESTING SCRIPT FOR LIQUIDATIONRETRACE STRATEGY 🌙

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# =====================
# DATA PREPARATION 🌌
# =====================
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns
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


# =====================
# STRATEGY CLASS 🌠
# =====================
class LiquidationRetrace(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    sma_period = 200
    rsi_period = 14
    swing_window = 20
    volume_multiplier = 1.5

    def init(self):
        # Core Indicators 🌗
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_window)
        self.swing_high = self.I(
            talib.MAX, self.data.High, timeperiod=self.swing_window
        )
        self.vol_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

    def next(self):
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Entry Conditions 🌊
        if not self.position:
            # Liquidation Event Proxy (Price below SMA + Volume Spike)
            liquidation_trigger = (current_close < self.sma200[-1]) and (
                current_volume > self.vol_ma[-1] * self.volume_multiplier
            )

            # SMA Retest (Wick below SMA + Close above)
            price_retest = (self.data.Low[-1] <= self.sma200[-1]) and (
                current_close > self.sma200[-1]
            )

            # RSI Crossover Condition
            rsi_trigger = (
                (self.rsi[-2] < 30) and (self.rsi[-1] > 30)
                if len(self.rsi) > 1
                else False
            )

            if liquidation_trigger and price_retest and rsi_trigger:
                # Risk Management Calculations 🛡️
                risk_amount = self.equity * self.risk_percent
                swing_stop = self.swing_low[-1]
                sma_stop = self.sma200[-1] * 0.99
                stop_price = min(swing_stop, sma_stop)

                risk_per_unit = current_close - stop_price
                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_price)
                        print(
                            f"🌙✨ MOON DEV ENTRY ✨🌙 | Price: {current_close:.2f} | Size: {position_size} | RSI: {self.rsi[-1]:.1f}"
                        )

        # Exit Conditions 🏁
        else:
            resistance_level = self.swing_high[-1]
            volume_spike = current_volume > self.vol_ma[-1] * self.volume_multiplier

            if current_close >= resistance_level and volume_spike:
                self.position.close()
                print(
                    f"🚀🌕 PROFIT TAKEN 🌕🚀 | Exit Price: {current_close:.2f} | Resistance: {resistance_level:.2f}"
                )


# =====================
# BACKTEST EXECUTION 🚀
# =====================
bt = Backtest(data, LiquidationRetrace, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 40)
print("🌙 MOON DEV FINAL STATS 🌙")
print("=" * 40)
print(stats)
print("\nSTRATEGY DETAILS:")
print(stats._strategy)
