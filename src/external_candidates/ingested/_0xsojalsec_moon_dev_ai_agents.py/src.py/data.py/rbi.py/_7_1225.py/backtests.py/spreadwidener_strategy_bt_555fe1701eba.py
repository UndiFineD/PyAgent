# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\SpreadWidener_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class SpreadWidenerStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating SpreadWidener strategy! 🚀")
        self.spread = self.I(lambda h, l: h - l, self.data.High, self.data.Low)
        self.avg_spread = self.I(talib.SMA, self.spread, 20)
        self.std_spread = self.I(talib.STDDEV, self.spread, 20)
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_i = None

    def next(self):
        if self.position:
            bars_since = self._i - self.entry_i
            if bars_since > 120:  # approx 30 min
                print("🌙 Moon Dev time-based exit! Closing position. ✨")
                self.position.close()
                return
            if self.spread[-1] < self.avg_spread[-1] + 0.5 * self.std_spread[-1]:
                print("🌙 Moon Dev spread tightening! Closing position. ✨")
                self.position.close()
                return

        if (
            self.spread[-1] > self.avg_spread[-1] + 2.5 * self.std_spread[-1]
            and self.data.Volume[-1] > self.avg_volume[-1]
        ):
            print("🌙 Moon Dev detected wide spread! Preparing short entry. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                print("🌙 Moon Dev invalid risk calculation, skipping. ⚠️")
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 2 * risk_per_unit
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                self.entry_i = self._i
                print(
                    f"🌙 Moon Dev entered short with size {position_size}! SL: {sl}, TP: {tp} ✨"
                )
            else:
                print("🌙 Moon Dev position size too small, skipping. ⚠️")


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

bt = Backtest(data, SpreadWidenerStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
