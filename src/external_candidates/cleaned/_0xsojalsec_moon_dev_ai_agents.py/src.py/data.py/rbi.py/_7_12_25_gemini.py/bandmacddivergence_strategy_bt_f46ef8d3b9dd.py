# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandMACDDivergence_strategy_bt.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def upper_band_slope(upper_band_series, period=5):
    # Use numpy's polyfit to calculate the slope of the last 'period' points.
    # A positive slope indicates the band is trending upwards.
    if len(upper_band_series) < period:
        return 0
    y = upper_band_series[-period:]
    x = np.arange(len(y))
    # Returns slope and intercept, we only need the slope (first element).
    slope, _ = np.polyfit(x, y, 1)
    return slope


def lower_band_slope(lower_band_series, period=5):
    if len(lower_band_series) < period:
        return 0
    y = lower_band_series[-period:]
    x = np.arange(len(y))
    slope, _ = np.polyfit(x, y, 1)
    return slope


class BandMACDDivergenceStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandMACDDivergence strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # Calculate slopes as custom indicators
        self.upper_slope = self.I(upper_band_slope, self.upper, 5)
        self.lower_slope = self.I(lower_band_slope, self.lower, 5)

    def next(self):
        if self.position:
            if self.position.is_long and self.macd[-1] < self.macdsignal[-1]:
                print("🌙 Moon Dev MACD crossover against long! Closing position. ✨")
                self.position.close()
            elif self.position.is_short and self.macd[-1] > self.macdsignal[-1]:
                print("🌙 Moon Dev MACD crossover against short! Closing position. ✨")
                self.position.close()
            return

        # Long Entry: Uptrending BB, bullish MACD momentum
        is_uptrend = self.upper_slope[-1] > 0
        is_above_middle = self.data.Close[-1] > self.middle[-1]
        is_bullish_momentum = self.macdhist[-1] > self.macdhist[-2]

        if is_uptrend and is_above_middle and is_bullish_momentum:
            print("🌙 Moon Dev bullish BandMACDDivergence setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 3 * self.atr[-1]  # 1.5 R:R
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry: Downtrending BB, bearish MACD momentum
        is_downtrend = self.lower_slope[-1] < 0
        is_below_middle = self.data.Close[-1] < self.middle[-1]
        is_bearish_momentum = self.macdhist[-1] < self.macdhist[-2]

        if is_downtrend and is_below_middle and is_bearish_momentum:
            print("🌙 Moon Dev bearish BandMACDDivergence setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 3 * self.atr[-1]  # 1.5 R:R
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


if __name__ == "__main__":
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

    bt = Backtest(data, BandMACDDivergenceStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
