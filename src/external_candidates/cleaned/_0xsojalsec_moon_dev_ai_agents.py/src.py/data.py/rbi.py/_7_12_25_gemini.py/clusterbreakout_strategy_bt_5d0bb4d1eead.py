# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\ClusterBreakout_strategy_bt.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def find_volume_cluster(high, low, volume, period=10):
    if len(high) < period:
        return None, None

    # Get the most recent 'period' of data
    recent_highs = high[-period:]
    recent_lows = low[-period:]
    recent_volumes = volume[-period:]

    price_range_top = np.max(recent_highs)
    price_range_bottom = np.min(recent_lows)

    # This is a simplification. A real volume profile would be more complex.
    # We're finding the price level within this range that had the most volume.
    # For this simplified model, we'll just use the range itself.
    return price_range_top, price_range_bottom


class ClusterBreakoutStrategy(Strategy):
    cluster_period = 10

    def init(self):
        print("🌙 Moon Dev initiating ClusterBreakout strategy! 🚀")
        self.sma50 = self.I(talib.SMA, self.data.Close, 50)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if len(self.data.Close) < self.cluster_period:
            return

        if self.position:
            return

        cluster_top, cluster_bottom = find_volume_cluster(
            self.data.High, self.data.Low, self.data.Volume, self.cluster_period
        )
        if cluster_top is None:
            return

        volume_spike = self.data.Volume[-1] > 1.5 * self.volume_sma[-1]

        # Long Entry
        is_uptrend = self.data.Close[-1] > self.sma50[-1]
        is_breakout_up = self.data.Close[-1] > cluster_top

        if is_uptrend and is_breakout_up and volume_spike:
            print("🌙 Moon Dev bullish ClusterBreakout setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = cluster_top - self.atr[-1]  # Stop below breakout level
            tp = entry_price + 2 * (entry_price - sl)  # 2:1 R:R
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry
        is_downtrend = self.data.Close[-1] < self.sma50[-1]
        is_breakout_down = self.data.Close[-1] < cluster_bottom

        if is_downtrend and is_breakout_down and volume_spike:
            print("🌙 Moon Dev bearish ClusterBreakout setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = cluster_bottom + self.atr[-1]  # Stop above breakout level
            tp = entry_price - 2 * (sl - entry_price)  # 2:1 R:R
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

    bt = Backtest(data, ClusterBreakoutStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
