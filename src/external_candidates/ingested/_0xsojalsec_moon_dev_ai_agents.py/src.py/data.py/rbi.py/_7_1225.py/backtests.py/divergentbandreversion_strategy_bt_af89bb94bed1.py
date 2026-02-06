# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\DivergentBandReversion_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DivergentBandReversionStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DivergentBandReversion strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.price_low = self.I(talib.MIN, self.data.Low, 20)
        self.macd_low = self.I(talib.MIN, self.hist, 20)
        self.price_high = self.I(talib.MAX, self.data.High, 20)
        self.macd_high = self.I(talib.MAX, self.hist, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_i = None

    def next(self):
        if self.position:
            bars_since = (len(self.data) - 1) - self.entry_i
            close_condition = False
            if self.position.is_long:
                close_condition = self.data.Close[-1] >= self.middle[-1]
            elif self.position.is_short:
                close_condition = self.data.Close[-1] <= self.middle[-1]
            if bars_since > 10 or close_condition:
                print("🌙 Moon Dev reversion or time exit! Closing position. ✨")
                self.position.close()
            return

        bullish_div = (self.price_low[-1] < self.price_low[-2]) and (
            self.macd_low[-1] > self.macd_low[-2]
        )
        if bullish_div and self.data.Close[-1] > self.upper[-1]:
            print(
                "🌙 Moon Dev bullish divergent breakout! Entering short for reversion. 🚀"
            )
            entry_price = self.data.Close[-1]
            sl = self.upper[-1] + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = self.middle[-1]
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                self.entry_i = len(self.data) - 1
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")

        bearish_div = (self.price_high[-1] > self.price_high[-2]) and (
            self.macd_high[-1] < self.macd_high[-2]
        )
        if bearish_div and self.data.Close[-1] < self.lower[-1]:
            print(
                "🌙 Moon Dev bearish divergent breakout! Entering long for reversion. 🚀"
            )
            entry_price = self.data.Close[-1]
            sl = self.lower[-1] - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = self.middle[-1]
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                self.entry_i = len(self.data) - 1
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

bt = Backtest(
    data, DivergentBandReversionStrategy, cash=1000000, margin=1, commission=0.001
)
stats = bt.run()
print(stats)
print(stats._strategy)
