# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_04_2025\backtests_final\VolatilityPulse_BTFinal.py
# 🌙 Moon Dev's VolatilityPulse Backtest Implementation 🚀 (Debugged Version)

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Data cleansing ritual 🌌
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Column mapping alignment ✨
required_columns = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data.rename(columns=required_columns, inplace=True)


class VolatilityPulse(Strategy):
    atr_period = 5
    atr_ma_period = 20
    vix_lookback = 960  # 10 days in 15-min intervals (96*10)
    risk_pct = 0.01

    def init(self):
        # 🌙 Volatility Pulse Indicators
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.atr_ma = self.I(talib.SMA, self.atr, self.atr_ma_period)

        # Check if VIX column exists before creating indicator
        if hasattr(self.data, "vix"):
            self.vix_low = self.I(talib.MIN, self.data.vix, self.vix_lookback)
        else:
            raise ValueError("🌑 MOON ALERT: VIX data not found in dataset!")

        print("🌌 Moon Dev Indicators Activated: ATR(5), ATR_MA(20), VIX_LOW(960) ✨")

    def next(self):
        # Skip early bars where indicators are warming up
        if len(self.data) < self.vix_lookback:
            return

        # 🌙 Current market state
        current_atr = self.atr[-1]
        current_vix = self.data.vix[-1]
        vix_low = self.vix_low[-1]

        # 🚀 Long Entry Conditions
        if not self.position:
            # ATR crossover + VIX filter (Moon Dev's custom crossover implementation)
            if (self.atr[-2] < self.atr_ma[-2] and self.atr[-1] > self.atr_ma[-1]) and (
                current_vix < vix_low
            ):
                # Moon-sized risk calculation 💰
                risk_amount = self.equity * self.risk_pct
                stop_distance = 2 * current_atr

                if stop_distance > 0:
                    position_size = int(round(risk_amount / stop_distance))
                    if position_size > 0:
                        self.buy(size=position_size)
                        self.highest_high = self.data.High[
                            -1
                        ]  # Track for trailing stop
                        print(
                            f"🌕 MOON ENTRY! Size: {position_size} units @ {self.data.Close[-1]:.2f}"
                        )

        # 🌑 Trailing Stop Management
        if self.position.is_long:
            # Update highest high
            if self.data.High[-1] > self.highest_high:
                self.highest_high = self.data.High[-1]
                print(f"🚀 New Cosmic High: {self.highest_high:.2f}")

            # Calculate dynamic stop
            trailing_stop = self.highest_high - (2 * current_atr)

            # Exit if price breaches stop
            if self.data.Low[-1] < trailing_stop:
                self.position.close()
                print(
                    f"🌑 STOPPED OUT! Profit: {self.position.pl:.2f} | Exit @ {trailing_stop:.2f}"
                )


# 🌙 Launch Backtest Sequence
try:
    bt = Backtest(
        data, VolatilityPulse, cash=1_000_000, commission=0.002, exclusive_orders=True
    )
    stats = bt.run()
    print("\n🌙✨ MOON DEV FINAL STATS ✨🌙")
    print(stats)
    print(stats._strategy)
except Exception as e:
    print(f"🌑 CRITICAL MOON FAILURE: {str(e)}")
    print("✨ Check your data and indicators for alignment with cosmic forces!")

# 🌙 Debugging Notes:
# 1. Added VIX data existence check
#
