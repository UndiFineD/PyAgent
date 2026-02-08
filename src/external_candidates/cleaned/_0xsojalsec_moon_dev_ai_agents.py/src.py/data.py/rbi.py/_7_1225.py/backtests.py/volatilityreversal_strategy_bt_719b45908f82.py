# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\VolatilityReversal_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class VolatilityReversalStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating VolatilityReversal strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.width = self.I(lambda u, l: u - l, self.upper, self.lower)
        self.macd, self.signal, self.hist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.channel_upper = self.I(talib.MAX, self.data.High, 20)
        self.channel_lower = self.I(talib.MIN, self.data.Low, 20)
        self.avg_atr = self.I(talib.SMA, self.atr, 20)

    def next(self):
        if self.position:
            if self.data.Close[-1] > self.channel_upper[-1] or self.atr[-1] > 1.5 * self.avg_atr[-1]:
                print("🌙 Moon Dev exit signal! Closing position. ✨")
                self.position.close()
            return

        bb_expanding = self.width[-1] > self.width[-2]
        if (
            crossover(self.signal, self.macd)
            and bb_expanding
            and self.rsi[-1] < 30
            and self.data.Close[-1] <= self.lower[-1]
        ):
            print("🌙 Moon Dev detected volatility reversal! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.channel_lower[-1] - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + 2 * self.atr[-1]
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

bt = Backtest(data, VolatilityReversalStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
