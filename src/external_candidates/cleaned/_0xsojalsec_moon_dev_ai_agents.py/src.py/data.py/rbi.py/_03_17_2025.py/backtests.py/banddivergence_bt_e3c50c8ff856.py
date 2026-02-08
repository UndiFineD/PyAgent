# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_17_2025\backtests\BandDivergence_BT.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Moon Dev Data Preparation Ritual 🌙✨
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Cleanse column names with lunar magic 🧹🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Align cosmic coordinates 🌌📊
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


class BandDivergence(Strategy):
    def init(self):
        # Cosmic Indicator Calculations 🌙✨
        close = self.data.Close

        # Bollinger Bands with stardust parameters 🌠
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        self.upper_band = self.I(lambda: upper, name="UPPER")
        self.middle_band = self.I(lambda: middle, name="MIDDLE")
        self.lower_band = self.I(lambda: lower, name="LOWER")

        # MACD Histogram for divergence detection 🌗📉
        _, _, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.macd_hist = self.I(lambda: macdhist, name="MACD_HIST")

        self.trade_duration = 0

    def next(self):
        # Require sufficient cosmic history 🌌⏳
        if len(self.data) < 35:
            return

        # Current celestial readings 🌕📡
        current_close = self.data.Close[-1]
        prev_close = self.data.Close[-2]
        current_upper = self.upper_band[-1]
        prev_upper = self.upper_band[-2]

        # Cross above upper band detection 🌙🚀
        cross_above = (prev_close < prev_upper) and (current_close > current_upper)

        # Bullish MACD divergence check 🌗📈
        hist = self.macd_hist
        bullish_div = hist[-3] < hist[-2] < hist[-1]

        # Moon Dev Entry Protocol 🌙💼
        if not self.position and cross_above and bullish_div:
            # Cosmic risk calculations 🌌⚖️
            risk_pct = 0.01
            entry_price = current_close
            stop_price = current_upper * 1.005
            take_profit = self.middle_band[-1]

            risk_per_unit = stop_price - entry_price
            if risk_per_unit <= 0:
                return  # Avoid black hole scenarios 🕳️

            position_size = int(round((self.equity * risk_pct) / risk_per_unit))

            if position_size > 0:
                self.sell(size=position_size, sl=stop_price, tp=take_profit)
                self.trade_duration = 0
                print(f"🌙✨ MOON SHORT ACTIVATED! ✨")
                print(f"Entry: {entry_price:.2f} | SL: {stop_price:.2f} | TP: {take_profit:.2f}")
                print(f"Cosmic Position Size: {position_size} units 🚀")

        # Time-based exit after 10 lunar cycles ⏰🌙
        if self.position:
            self.trade_duration += 1
            if self.trade_duration >= 10:
                self.position.close()
                print(f"⏳🌙 TIME PORTAL CLOSED after 10 cycles")


# Launch Backtest Rocket 🚀📊
bt = Backtest(data, BandDivergence, cash=1_000_000, commission=0.002)
stats = bt.run()

# Display Cosmic Performance Report 🌌📜
print("\n🌠🌠🌠 MOON DEV BACKTEST RESULTS 🌠🌠🌠")
print(stats)
print("\n✨ Strategy Cosmic Secrets ✨")
print(stats._strategy)
