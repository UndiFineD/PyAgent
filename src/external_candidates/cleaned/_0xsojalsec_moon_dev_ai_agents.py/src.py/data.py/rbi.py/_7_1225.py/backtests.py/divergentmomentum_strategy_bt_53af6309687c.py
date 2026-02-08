# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\DivergentMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DivergentMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DivergentMomentum strategy! 🚀")
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.ma50 = self.I(talib.SMA, self.data.Close, 50)
        self.cci = self.I(talib.CCI, self.data.High, self.data.Low, self.data.Close, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.rsi_low = self.I(talib.MIN, self.rsi, 20)
        self.price_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if self.position:
            if self.cci[-1] > 100 and self.cci[-1] < self.cci[-2]:
                print("🌙 Moon Dev CCI turning down! Closing position. ✨")
                self.position.close()
            return

        bullish_div = (self.rsi_low[-1] > self.rsi_low[-2]) and (self.price_low[-1] < self.price_low[-2])
        if self.rsi[-1] < 30 and bullish_div and self.data.Close[-1] > self.ma50[-1]:
            print("🌙 Moon Dev detected divergent momentum! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.data.Low[-1] - 0.01 * entry_price
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + risk_per_unit
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! SL: {sl}, TP: {tp} ✨")


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

bt = Backtest(data, DivergentMomentumStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
