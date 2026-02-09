# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_final\ExtremeDivergence_BTFinal_v1.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from scipy.signal import argrelextrema

# Load and prepare data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)
data.columns = data.columns.str.strip().str.lower()
data = data.loc[:, ~data.columns.str.contains("^unnamed", case=False)]
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)
data = data.set_index(pd.to_datetime(data["datetime"]))
data.sort_index(inplace=True)
data = data.dropna()


class ExtremeDivergence(Strategy):
    def init(self):
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)
        macd_line, signal_line, hist = self.I(
            talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.hist = hist
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0

    def next(self):
        if self.i < 10:
            return
        # Compute trend
        ema_slope = self.ema200[self.i] - self.ema200[self.i - 10]
        uptrend = self.data.Close[self.i] > self.ema200[self.i] and ema_slope > 0
        downtrend = self.data.Close[self.i] < self.ema200[self.i] and ema_slope < 0

        # Compute bullish hidden divergence
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[: self.i + 1]
        low_indices = argrelextrema(price_slice_low, np.less_equal, order=5)[0]
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 > p1 and h2 < h1:
                    bullish_div = True
                    recent_swing_low = p2

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[: self.i + 1]
        high_indices = argrelextrema(price_slice_high, np.greater_equal, order=5)[0]
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 < p1 and h2 > h1:
                    bearish_div = True
                    recent_swing_high = p2

        # Entry logic
        if not self.position:
            if uptrend and bullish_div and self.rsi[self.i] < 30:
                entry = self.data.Close[self.i]
                atr_val = self.atr[self.i]
                sl = recent_swing_low - 1.5 * atr_val
                risk_dist = entry - sl
                if risk_dist > 0:
                    size = (self.equity * 0.01) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.buy(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.highest = self.data.High[self.i]
                        print(
                            f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨🚀"
                        )
            elif downtrend and bearish_div and self.rsi[self.i] > 70:
                entry = self.data.Close[self.i]
                atr_val = self.atr[self.i]
                sl = recent_swing_high + 1.5 * atr_val
                risk_dist = sl - entry
                if risk_dist > 0:
                    size = (self.equity * 0.01) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.sell(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.lowest = self.data.Low[self.i]
                        print(
                            f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨📉"
                        )

        # Exit logic
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[self.i])
                new_trail = self.highest - 2 * self.atr[self.i]
                self.trail_sl = max(self.trail_sl, new_trail)
                exit_reason = None
                if self.data.Low[self.i] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[self.i] > 70:
                    exit_reason = "RSI Overbought"
                elif self.data.Close[self.i] < self.ema200[self.i]:
                    exit_reason = "EMA Cross Below"
                if exit_reason:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long Exit at {self.data.Close[self.i]:.2f} - Reason: {exit_reason} 💥"
                    )
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[self.i])
                new_trail = self.lowest + 2 * self.atr[self.i]
                self.trail_sl = min(self.trail_sl, new_trail)
                exit_reason = None
                if self.data.High[self.i] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[self.i] < 30:
                    exit_reason = "RSI Oversold"
                elif self.data.Close[self.i] > self.ema200[self.i]:
                    exit_reason = "EMA Cross Above"
                if exit_reason:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Short Exit at {self.data.Close[self.i]:.2f} - Reason: {exit_reason} 💥"
                    )


# Run backtest
bt = Backtest(
    data, ExtremeDivergence, cash=1000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
print(stats._strategy)
