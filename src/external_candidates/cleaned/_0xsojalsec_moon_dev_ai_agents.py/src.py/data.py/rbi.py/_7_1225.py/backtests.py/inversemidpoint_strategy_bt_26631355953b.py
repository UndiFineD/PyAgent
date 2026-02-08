# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\InverseMidpoint_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class InverseMidpointStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating InverseMidpoint strategy! 🚀")
        self.midpoint = self.I(lambda o, h: (o.s - 1 + h.s - 1) / 2, self.data.Open, self.data.High)
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            if self.data.Close[-1] > self.midpoint[-1] or self.data.Volume[-1] < 1.1 * self.avg_volume[-1]:
                print("🌙 Moon Dev exit condition met! Closing short. ✨")
                self.position.close()
            return

        if self.data.Close[-1] < self.midpoint[-1] and self.data.Volume[-1] > 1.1 * self.avg_volume[-1]:
            print("🌙 Moon Dev detected bearish setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.midpoint[-1] + 0.01 * self.midpoint[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 2 * risk_per_unit
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! SL: {sl}, TP: {tp} ✨")


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

daily_data = data.resample("D").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
print("🌙 Moon Dev resampled to daily data! ✨")

bt = Backtest(daily_data, InverseMidpointStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
