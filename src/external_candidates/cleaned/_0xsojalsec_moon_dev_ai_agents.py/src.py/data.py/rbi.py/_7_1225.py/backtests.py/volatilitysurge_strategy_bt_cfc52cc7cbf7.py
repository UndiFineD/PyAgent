# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\VolatilitySurge_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class VolatilitySurgeStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating VolatilitySurge strategy! 🚀")
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.upper_level = self.I(talib.MAX, self.data.High, 20)
        self.lower_level = self.I(talib.MIN, self.data.Low, 20)
        self.sma = self.I(talib.SMA, self.data.Close, 50)

    def next(self):
        if self.position:
            return

        low_vol = self.atr[-1] < 0.01 * self.data.Close[-1]
        if low_vol and self.data.Close[-1] > self.upper_level[-1] and self.data.Close[-1] > self.sma[-1]:
            print("🌙 Moon Dev detected upside surge! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.lower_level[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + 2 * self.atr[-1]
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        if low_vol and self.data.Close[-1] < self.lower_level[-1] and self.data.Close[-1] < self.sma[-1]:
            print("🌙 Moon Dev detected downside surge! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.upper_level[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 2 * self.atr[-1]
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

bt = Backtest(data, VolatilitySurgeStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
