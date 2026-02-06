# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\FibroMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class FibroMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating FibroMomentum strategy! 🚀")
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            return

        sh = self.swing_high[-1]
        sl = self.swing_low[-1]
        retrace_50 = sl + 0.5 * (sh - sl)

        if (
            abs(self.data.Close[-1] - retrace_50) < self.atr[-1]
            and self.rsi[-1] < 50
            and self.hist[-1] < 0
        ):
            print("🌙 Moon Dev detected Fib reversal! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 1.5 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            extension_127 = sl + 1.272 * (sh - sl)
            tp = extension_127
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(
                    f"🌙 Moon Dev entered long with size {position_size}! SL: {sl}, TP: {tp} ✨"
                )


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

bt = Backtest(data, FibroMomentumStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
