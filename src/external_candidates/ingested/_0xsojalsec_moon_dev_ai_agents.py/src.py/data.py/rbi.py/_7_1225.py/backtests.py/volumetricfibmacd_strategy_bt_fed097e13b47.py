# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\VolumetricFibMACD_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class VolumetricFibMACDStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating VolumetricFibMACD strategy! 🚀")
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.ema26 = self.I(talib.EMA, self.data.Close, 26)
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.avg_atr = self.I(talib.SMA, self.atr, 20)

    def next(self):
        if self.position:
            return

        sh = self.swing_high[-1]
        sl = self.swing_low[-1]
        retrace_382 = sh - 0.382 * (sh - sl)

        if (
            crossover(self.signal, self.ema26)
            and abs(self.data.Close[-1] - retrace_382) < self.atr[-1]
            and self.data.Volume[-1] > self.avg_volume[-1]
            and self.atr[-1] > 1.5 * self.avg_atr[-1]
        ):
            print("🌙 Moon Dev volumetric Fib MACD signal! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = sl - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            extension_618 = sl + 0.618 * (sh - sl)
            tp = extension_618
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        retrace_382_short = sl + 0.382 * (sh - sl)
        if (
            crossover(self.ema26, self.signal)
            and abs(self.data.Close[-1] - retrace_382_short) < self.atr[-1]
            and self.data.Volume[-1] > self.avg_volume[-1]
            and self.atr[-1] > 1.5 * self.avg_atr[-1]
        ):
            print("🌙 Moon Dev volumetric Fib MACD signal! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = sh + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            extension_618_short = sh - 0.618 * (sh - sl)
            tp = extension_618_short
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

bt = Backtest(data, VolumetricFibMACDStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
