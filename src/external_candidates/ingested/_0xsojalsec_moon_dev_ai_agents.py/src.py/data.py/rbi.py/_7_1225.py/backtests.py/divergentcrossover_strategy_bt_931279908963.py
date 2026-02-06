# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\DivergentCrossover_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DivergentCrossoverStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DivergentCrossover strategy! 🚀")
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.cci = self.I(talib.CCI, self.data.High, self.data.Low, self.data.Close, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.rsi_high = self.I(talib.MAX, self.rsi, 20)
        self.rsi_low = self.I(talib.MIN, self.rsi, 20)
        self.price_high = self.I(talib.MAX, self.data.High, 20)
        self.price_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if self.position:
            if (self.position.is_long and self.cci[-1] > 100) or (
                self.position.is_short and self.cci[-1] < -100
            ):
                print("🌙 Moon Dev CCI extreme! Closing position. ✨")
                self.position.close()
            return

        bullish_div = (self.rsi_low[-1] > self.rsi_low[-2]) and (
            self.price_low[-1] < self.price_low[-2]
        )
        if (
            bullish_div
            and crossover(self.macd, self.signal)
            and self.hist[-1] > 0
            and self.cci[-1] < 100
        ):
            print("🌙 Moon Dev bullish divergent crossover! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.price_low[-1] - self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + risk_per_unit
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        bearish_div = (self.rsi_high[-1] < self.rsi_high[-2]) and (
            self.price_high[-1] > self.price_high[-2]
        )
        if (
            bearish_div
            and crossover(self.signal, self.macd)
            and self.hist[-1] < 0
            and self.cci[-1] > -100
        ):
            print("🌙 Moon Dev bearish divergent crossover! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.price_high[-1] + self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - risk_per_unit
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

bt = Backtest(
    data, DivergentCrossoverStrategy, cash=1000000, margin=1, commission=0.001
)
stats = bt.run()
print(stats)
print(stats._strategy)
