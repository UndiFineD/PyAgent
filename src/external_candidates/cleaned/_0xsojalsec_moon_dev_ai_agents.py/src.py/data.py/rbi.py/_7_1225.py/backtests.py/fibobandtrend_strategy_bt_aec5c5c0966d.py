# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\FiboBandTrend_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class FiboBandTrendStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating FiboBandTrend strategy! 🚀")
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            if (self.position.is_long and self.data.Close[-1] > self.middle[-1]) or (
                self.position.is_short and self.data.Close[-1] < self.middle[-1]
            ):
                print("🌙 Moon Dev price reverted to middle band! Closing position. ✨")
                self.position.close()
            return

        sh = self.swing_high[-1]
        sl = self.swing_low[-1]
        retrace_618 = sh - 0.618 * (sh - sl)
        if self.data.Close[-1] <= self.lower[-1] and abs(self.data.Close[-1] - retrace_618) < self.atr[-1]:
            print("🌙 Moon Dev Fib band confluence! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = sl - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            extension_1618 = sl + 1.618 * (sh - sl)
            tp = extension_1618
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        retrace_618_short = sl + 0.618 * (sh - sl)
        if self.data.Close[-1] >= self.upper[-1] and abs(self.data.Close[-1] - retrace_618_short) < self.atr[-1]:
            print("🌙 Moon Dev Fib band confluence! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = sh + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            extension_1618_short = sh - 1.618 * (sh - sl)
            tp = extension_1618_short
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

bt = Backtest(data, FiboBandTrendStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
