# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\VolumeSkewDivergence_strategy_bt.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class VolumeSkewDivergenceStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating VolumeSkewDivergence strategy! 🚀")
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.avg_price = self.I(talib.SMA, self.data.Close, 20)
        self.volume_div = self.I(
            lambda v, av: (v - av) / av if av != 0 else 0,
            self.data.Volume,
            self.avg_volume,
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.resistance = self.I(talib.MAX, self.data.High, 20)
        self.support = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if self.position:
            if self.volume_div[-1] < 1:
                print("🌙 Moon Dev skew decreasing! Closing position. ✨")
                self.position.close()
            return

        if self.volume_div[-1] > 2 and self.data.Close[-1] > self.avg_price[-1]:
            print("🌙 Moon Dev volume skew divergence! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.support[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + self.atr[-1]
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")


data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
print("🌙 Moon Dev loading BTC-USD data... 🚀")
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
print("🌙 Moon Dev data cleaning complete! ✨")

bt = Backtest(data, VolumeSkewDivergenceStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
