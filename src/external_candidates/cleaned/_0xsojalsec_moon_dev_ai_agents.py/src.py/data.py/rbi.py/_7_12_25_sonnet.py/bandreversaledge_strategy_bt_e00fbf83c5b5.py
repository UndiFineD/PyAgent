# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandReversalEdge_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandReversalEdgeStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandReversalEdge strategy! 🚀")
        self.upper_bb_50, self.middle_bb_50, self.lower_bb_50 = self.I(talib.BBANDS, self.data.Close, 50, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_bar = 0

    def next(self):
        if self.position:
            # Exit conditions: 3-bar window or upper BB touch
            bars_since_entry = len(self.data) - self.entry_bar
            if bars_since_entry >= 3 or self.data.Close[-1] >= self.upper_bb_50[-1]:
                print("🌙 Moon Dev BandReversalEdge exit trigger! Closing position. ✨")
                self.position.close()
            return

        # Entry conditions: 50-period BB above price + price below lower BB
        bb_above_price = self.upper_bb_50[-1] > self.data.Close[-1]
        price_below_lower_bb = self.data.Close[-1] < self.lower_bb_50[-1]

        if bb_above_price and price_below_lower_bb:
            print("🌙 Moon Dev BandReversalEdge setup detected! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 0.5 * self.atr[-1]
            # No take profit - will exit on time or upper BB touch
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl)
                self.entry_bar = len(self.data)
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

bt = Backtest(data, BandReversalEdgeStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
