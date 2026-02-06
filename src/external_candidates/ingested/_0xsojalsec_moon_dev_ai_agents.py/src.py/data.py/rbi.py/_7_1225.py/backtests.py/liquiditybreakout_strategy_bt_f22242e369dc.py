# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\LiquidityBreakout_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class LiquidityBreakoutStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating LiquidityBreakout strategy! 🚀")
        self.resistance = self.I(talib.MAX, self.data.High, 20)
        self.support = self.I(talib.MIN, self.data.Low, 20)
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            return

        if (
            self.data.Close[-1] > self.resistance[-1]
            and self.data.Volume[-1] > 1.5 * self.avg_volume[-1]
        ):
            print("🌙 Moon Dev detected upside breakout! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.support[-1] - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + self.atr[-1] * 2
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(
                    f"🌙 Moon Dev entered long with size {position_size}! SL: {sl}, TP: {tp} ✨"
                )

        if (
            self.data.Close[-1] < self.support[-1]
            and self.data.Volume[-1] > 1.5 * self.avg_volume[-1]
        ):
            print("🌙 Moon Dev detected downside breakout! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.resistance[-1] + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - self.atr[-1] * 2
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(
                    f"🌙 Moon Dev entered short with size {position_size}! SL: {sl}, TP: {tp} ✨"
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

bt = Backtest(data, LiquidityBreakoutStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
