# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandSqueezeTrend_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandSqueezeTrendStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandSqueezeTrend strategy! 🚀")
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.atr_ma = self.I(talib.SMA, self.atr, 20)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

    def next(self):
        if self.position:
            # Exit conditions
            if self.data.Close[-1] <= self.middle_bb[-1]:
                print("🌙 Moon Dev trend reversal! Closing position. ✨")
                self.position.close()
            return

        # Entry conditions for BandSqueezeTrend
        price_above_upper_bb = self.data.Close[-1] > self.upper_bb[-1]
        price_below_atr_ma = self.data.Close[-1] < self.atr_ma[-1]

        if price_above_upper_bb and price_below_atr_ma:
            print("🌙 Moon Dev BandSqueezeTrend setup detected! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 0.5 * self.atr[-1]
            tp = entry_price + 1.5 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
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

bt = Backtest(data, BandSqueezeTrendStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
