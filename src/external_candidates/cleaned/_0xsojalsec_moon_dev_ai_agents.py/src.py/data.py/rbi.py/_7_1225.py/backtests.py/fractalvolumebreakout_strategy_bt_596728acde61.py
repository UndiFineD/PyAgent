# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\FractalVolumeBreakout_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class FractalVolumeBreakoutStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating FractalVolumeBreakout strategy! 🚀")
        self.fractal_high = self.I(talib.MAX, self.data.High, 5)
        self.fractal_low = self.I(talib.MIN, self.data.Low, 5)
        self.vma = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            if self.data.Volume[-1] < self.vma[-1]:
                print("🌙 Moon Dev volume decreasing! Closing position. ✨")
                self.position.close()
            return

        if self.data.Close[-1] > self.fractal_high[-3] and self.data.Volume[-1] > 1.5 * self.vma[-1]:
            print("🌙 Moon Dev fractal breakout up! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.fractal_low[-1] - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = self.fractal_high[-1] + (self.fractal_high[-1] - self.fractal_low[-1])
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        if self.data.Close[-1] < self.fractal_low[-3] and self.data.Volume[-1] > 1.5 * self.vma[-1]:
            print("🌙 Moon Dev fractal breakout down! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.fractal_high[-1] + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = self.fractal_low[-1] - (self.fractal_high[-1] - self.fractal_low[-1])
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


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

bt = Backtest(data, FractalVolumeBreakoutStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
