# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandMACDDivergence_strategy_bt.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandMACDDivergenceStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandMACDDivergence strategy! 🚀")
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def bb_slope(self, data, period=5):
        """Calculate slope of Bollinger Band"""
        if len(data) < period:
            return 0
        return (data[-1] - data[-period]) / period

    def next(self):
        if self.position:
            # Exit on MACD signal reversal
            if (self.position.is_long and crossover(self.signal, self.macd)) or (
                self.position.is_short and crossover(self.macd, self.signal)
            ):
                print("🌙 Moon Dev MACD reversal! Closing position. ✨")
                self.position.close()
            return

        # Calculate upper BB slope
        bb_slope = self.bb_slope(self.upper_bb)

        # Long entry: steep BB slope with bullish MACD divergence
        steep_slope = bb_slope > 0.5  # Adjust threshold as needed
        macd_bullish = crossover(self.macd, self.signal)
        macd_divergence = abs(self.macd[-1] - self.macd[-5]) > 1.5 * self.atr[-1]

        if steep_slope and macd_bullish and macd_divergence:
            print("🌙 Moon Dev bullish BandMACD divergence! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short entry: flattening BB slope with bearish MACD divergence
        flat_slope = bb_slope < 0.2
        macd_bearish = crossover(self.signal, self.macd)

        if flat_slope and macd_bearish and macd_divergence:
            print("🌙 Moon Dev bearish BandMACD divergence! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 2 * self.atr[-1]
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

bt = Backtest(
    data, BandMACDDivergenceStrategy, cash=1000000, margin=1, commission=0.001
)
stats = bt.run()
print(stats)
print(stats._strategy)
