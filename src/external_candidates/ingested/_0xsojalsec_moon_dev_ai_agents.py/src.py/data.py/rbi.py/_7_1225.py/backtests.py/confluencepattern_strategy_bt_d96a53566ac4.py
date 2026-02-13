# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\ConfluencePattern_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ConfluencePatternStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating ConfluencePattern strategy! 🚀")
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            if (self.position.is_long and self.rsi[-1] > 70) or (
                self.position.is_short and self.rsi[-1] < 30
            ):
                print("🌙 Moon Dev RSI extreme! Closing position. ✨")
                self.position.close()
            return

        bullish_confluence = (
            self.data.Close[-1] > self.ema50[-1] > self.ema200[-1]
            and self.rsi[-1] > 50
            and crossover(self.macd, self.signal)
            and self.data.Volume[-1] > self.avg_volume[-1]
        )
        if bullish_confluence:
            print("🌙 Moon Dev bullish confluence! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + 2 * risk_per_unit
            adjusted = entry_price * (1 + 0.001)
            if tp <= adjusted:
                print(
                    "🌙 Moon Dev skipping long entry due to insufficient ATR for commission! 🚀"
                )
                return
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        bearish_confluence = (
            self.data.Close[-1] < self.ema50[-1] < self.ema200[-1]
            and self.rsi[-1] < 50
            and crossover(self.signal, self.macd)
            and self.data.Volume[-1] > self.avg_volume[-1]
        )
        if bearish_confluence:
            print("🌙 Moon Dev bearish confluence! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 2 * risk_per_unit
            adjusted = entry_price * (1 - 0.001)
            if tp >= adjusted:
                print(
                    "🌙 Moon Dev skipping short entry due to insufficient ATR for commission! 🚀"
                )
                return
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

bt = Backtest(data, ConfluencePatternStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
