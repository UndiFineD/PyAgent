# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandStrengthMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandStrengthMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandStrengthMomentum strategy! 🚀")
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # Using RSI as relative strength proxy
        self.relative_strength = self.I(talib.RSI, self.data.Close, 14)

    def next(self):
        if self.position:
            # Exit conditions
            if self.position.is_long:
                if self.data.Close[-1] >= self.upper_bb[-1] or self.relative_strength[-1] < 40:
                    print("🌙 Moon Dev long exit signal! Closing position. ✨")
                    self.position.close()
            elif self.position.is_short:
                if self.data.Close[-1] <= self.lower_bb[-1] or self.relative_strength[-1] > 60:
                    print("🌙 Moon Dev short exit signal! Closing position. ✨")
                    self.position.close()
            return

        # Long entry: Price crosses above lower BB + strong RS
        price_above_lower_bb = self.data.Close[-1] > self.lower_bb[-1] and self.data.Close[-2] <= self.lower_bb[-2]
        strong_momentum = self.relative_strength[-1] > 50

        if price_above_lower_bb and strong_momentum:
            print("🌙 Moon Dev bullish BandStrengthMomentum setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.lower_bb[-1]
            tp = self.upper_bb[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short entry: Price crosses below upper BB + weak RS
        price_below_upper_bb = self.data.Close[-1] < self.upper_bb[-1] and self.data.Close[-2] >= self.upper_bb[-2]
        weak_momentum = self.relative_strength[-1] < 50

        if price_below_upper_bb and weak_momentum:
            print("🌙 Moon Dev bearish BandStrengthMomentum setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.upper_bb[-1]
            tp = self.lower_bb[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
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

bt = Backtest(data, BandStrengthMomentumStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
