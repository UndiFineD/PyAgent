# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\CoTrendalNeutral_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class CoTrendalNeutralStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating CoTrendalNeutral strategy! 🚀")
        self.ma50 = self.I(talib.SMA, self.data.Close, 50)
        self.ma200 = self.I(talib.SMA, self.data.Close, 200)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr_ma = self.I(talib.SMA, self.atr, 50)

    def next(self):
        if self.position:
            return

        if self.data.Close[-1] > self.ma50[-1] and self.atr[-1] < self.atr_ma[-1]:
            print("🌙 Moon Dev co-trend long signal! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 3 * (entry_price - self.ma200[-1])
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + risk_per_unit * 3
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        if self.atr[-1] > self.atr_ma[-1] and self.data.Close[-1] > self.ma50[-1]:
            print("🌙 Moon Dev co-trend short signal! Entering short on volatility. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 3 * (entry_price - self.ma200[-1])
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - risk_per_unit * 3
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

bt = Backtest(data, CoTrendalNeutralStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
