# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandSyncMomentum_strategy_bt.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def middle_band_slope(middle_band_series, period=5):
    if len(middle_band_series) < period:
        return 0
    y = middle_band_series[-period:]
    x = np.arange(len(y))
    slope, _ = np.polyfit(x, y, 1)
    return slope


class BandSyncMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandSyncMomentum strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.middle_slope = self.I(middle_band_slope, self.middle, 5)

    def next(self):
        # --- Exit Logic ---
        if self.position:
            if self.position.is_long and self.data.Close[-1] >= self.upper[-1]:
                print("🌙 Moon Dev long hit upper band! Closing position. ✨")
                self.position.close()
            elif self.position.is_short and self.data.Close[-1] <= self.lower[-1]:
                print("🌙 Moon Dev short hit lower band! Closing position. ✨")
                self.position.close()
            # Alternative exit if trend flattens/reverses
            elif self.position.is_long and self.middle_slope[-1] < 0:
                self.position.close()
            elif self.position.is_short and self.middle_slope[-1] > 0:
                self.position.close()
            return

        # --- Entry Logic ---
        # Long Entry: Buy the dip in an uptrend
        is_uptrend = self.middle_slope[-1] > 0
        was_a_dip = self.data.Close[-2] <= self.lower[-2]
        is_recovering = self.data.Close[-1] > self.lower[-1]

        if is_uptrend and was_a_dip and is_recovering:
            print("🌙 Moon Dev bullish BandSyncMomentum setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry: Sell the rally in a downtrend
        is_downtrend = self.middle_slope[-1] < 0
        was_a_rally = self.data.Close[-2] >= self.upper[-2]
        is_reversing = self.data.Close[-1] < self.upper[-1]

        if is_downtrend and was_a_rally and is_reversing:
            print("🌙 Moon Dev bearish BandSyncMomentum setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl)
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

    bt = Backtest(data, BandSyncMomentumStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
