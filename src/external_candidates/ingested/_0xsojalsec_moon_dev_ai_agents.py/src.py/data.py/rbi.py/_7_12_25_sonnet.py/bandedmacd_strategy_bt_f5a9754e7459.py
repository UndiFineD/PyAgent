# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandedMACD_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandedMACDStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandedMACD strategy! 🚀")
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.recent_high = self.I(talib.MAX, self.data.High, 10)

    def next(self):
        # This strategy focuses on exit signals for existing long positions
        if self.position and self.position.is_long:
            # Exit on MACD bullish signal + price at upper BB + pullback
            macd_bullish = crossover(self.macd, self.signal)
            price_at_upper_bb = self.data.Close[-1] >= self.upper_bb[-1]
            pullback = self.data.Close[-1] < self.recent_high[-1]

            if macd_bullish and price_at_upper_bb and pullback:
                print("🌙 Moon Dev BandedMACD exit signal! Closing long position. ✨")
                self.position.close()
            return

        # Entry logic: Enter long when conditions are NOT met (for demo purposes)
        # In practice, this would be used with another entry strategy
        if not self.position:
            # Simple entry: price bounces off lower BB
            if (
                self.data.Close[-1] <= self.lower_bb[-1]
                and self.data.Close[-1] > self.data.Close[-2]
            ):
                print("🌙 Moon Dev entering long for BandedMACD management! 🚀")
                entry_price = self.data.Close[-1]
                sl = entry_price - 2 * self.atr[-1]
                tp = self.upper_bb[-1]
                risk_per_unit = entry_price - sl
                if risk_per_unit <= 0:
                    return
                risk_amount = self.equity * 0.01
                position_size = risk_amount / risk_per_unit
                position_size = int(round(position_size))
                if position_size > 0:
                    self.buy(size=position_size, sl=sl)
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

bt = Backtest(data, BandedMACDStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
