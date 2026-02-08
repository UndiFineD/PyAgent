# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\ForceChannelBreakout_BT.py
# 🌙 Moon Dev's ForceChannel Breakout Strategy Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🚀 Data Preparation with Moon-Style Cleaning 🚀
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# 🌌 Cosmic Data Cleansing 🌌
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class ForceChannelBreakout(Strategy):
    def init(self):
        # 🌠 Celestial Indicators 🌠
        self.fi = self.I(talib.FORCE, self.data.Close, self.data.Volume, 13, name="ForceIndex")
        self.ema20 = self.I(talib.EMA, self.data.Close, 20, name="EMA20")
        self.atr20 = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20, name="ATR20")
        self.upper_kc = self.I(lambda ema, atr: ema + 1.5 * atr, self.ema20, self.atr20, name="UpperKC")
        self.lower_kc = self.I(lambda ema, atr: ema - 1.5 * atr, self.ema20, self.atr20, name="LowerKC")
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="SwingLow")
        self.vol_sma = self.I(talib.SMA, self.data.Volume, 20, name="VolSMA")
        self.atr_sma = self.I(talib.SMA, self.atr20, 20, name="ATR_SMA")

    def next(self):
        # 🌑 Lunar Trade Logic 🌑
        price = self.data.Close[-1]
        fi_now, fi_prev = self.fi[-1], self.fi[-2] if len(self.fi) > 1 else 0
        atr_now = self.atr20[-1]
        atr_avg = self.atr_sma[-1]

        # 🌕 Entry Constellation 🌕
        if not self.position and all(
            [
                price > self.upper_kc[-1],
                fi_now > 0 and fi_prev <= 0,
                self.data.Volume[-1] > self.vol_sma[-1],
                atr_now > atr_avg,
            ]
        ):
            # 🌗 Risk Management Nebula 🌗
            entry_price = price
            stop_level = max(self.swing_low[-1], self.lower_kc[-1])
            stop_dist = entry_price - stop_level
            atr_dist = atr_now

            # Ensure minimum 1 ATR stop distance
            final_stop = entry_price - max(stop_dist, atr_dist)
            risk_amount = self.equity * 0.01  # 1% risk

            if (entry_price - final_stop) > 0:
                position_size = int(round(risk_amount / (entry_price - final_stop)))
                tp_level = entry_price + 2 * atr_dist

                self.buy(size=position_size, sl=final_stop, tp=tp_level, tag="MoonRocket")
                print(
                    f"🚀 LIFTOFF! Long {position_size} @ {entry_price:.2f} | SL: {final_stop:.2f} | TP: {tp_level:.2f}"
                )

        # 🌒 Exit Black Hole 🌒
        elif self.position and fi_now < 0 and fi_prev >= 0:
            self.position.close()
            print(f"🌑 GRAVITY WELL! Exiting @ {price:.2f}")


# 🌟 Launch Backtest 🌟
bt = Backtest(data, ForceChannelBreakout, cash=1_000_000, trade_on_close=True)
stats = bt.run()

# 📊 Print Cosmic Performance 📊
print("\n🌌 FINAL MISSION REPORT 🌌")
print(stats)
print(stats._strategy)
