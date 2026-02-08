# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v9.py
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
        # 🌙 Moon Dev Optimization: Switched to EMA50 for faster trend detection on 15m timeframe (was 200, too slow)
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)
        # 🌙 Added volume SMA for confirmation filter to avoid low-volume fakeouts
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # 🌙 Added ADX for trend strength filter to only trade in trending markets (avoid chop)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        macd_line, signal_line, hist = self.I(talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.hist = hist
        # 🌙 Moon Dev Optimization: Relaxed RSI threshold in entry (was <30/>70, too rare → <40/>60) to increase trade frequency
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0

    def next(self):
        current_len = len(self.ema50)
        # 🌙 Moon Dev Optimization: Reduced slope window to 5 periods for quicker trend response (was 11)
        if current_len < 5:
            return
        # Compute trend with EMA50 and shorter slope
        ema_slope = self.ema50[-1] - self.ema50[-5]
        uptrend = self.data.Close[-1] > self.ema50[-1] and ema_slope > 0
        downtrend = self.data.Close[-1] < self.ema50[-1] and ema_slope < 0

        # Compute bullish hidden divergence
        # 🌙 Moon Dev Optimization: Increased order=7 and min_dist=7 for stronger, less noisy swing detections (was 5/5)
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[:current_len].values
        low_indices = argrelextrema(price_slice_low, np.less_equal, order=7)[0]
        hist_slice = self.hist[:current_len]
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            if idx2 - idx1 >= 7:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                h1 = hist_slice.iloc[idx1]
                h2 = hist_slice.iloc[idx2]
                # 🌙 Added NaN check to avoid invalid early divergences
                if not (np.isnan(h1) or np.isnan(h2)) and p2 > p1 and h2 < h1:
                    bullish_div = True
                    recent_swing_low = p2

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[:current_len].values
        high_indices = argrelextrema(price_slice_high, np.greater_equal, order=7)[0]
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            if idx2 - idx1 >= 7:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                h1 = hist_slice.iloc[idx1]
                h2 = hist_slice.iloc[idx2]
                if not (np.isnan(h1) or np.isnan(h2)) and p2 < p1 and h2 > h1:
                    bearish_div = True
                    recent_swing_high = p2

        # Entry logic
        # 🌙 Moon Dev Optimization: Added volume > SMA20 and ADX >20 filters for higher quality entries
        # Increased risk to 2% (was 1%) for higher potential returns, with tighter SL to manage risk
        if not self.position:
            if (
                uptrend
                and bullish_div
                and self.rsi[-1] < 40
                and self.data.Volume[-1] > self.vol_sma[-1]
                and self.adx[-1] > 20
            ):
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                # 🌙 Tighter initial SL: 0.5 ATR below swing (was 1.5) for better risk-reward
                sl = recent_swing_low - 0.5 * atr_val
                risk_dist = entry - sl
                if risk_dist > 0:
                    # 🌙 Increased to 2% equity risk for amplified returns
                    size = (self.equity * 0.02) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.buy(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.highest = self.data.High[-1]
                        print(f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨🚀")
            elif (
                downtrend
                and bearish_div
                and self.rsi[-1] > 60
                and self.data.Volume[-1] > self.vol_sma[-1]
                and self.adx[-1] > 20
            ):
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_high + 0.5 * atr_val
                risk_dist = sl - entry
                if risk_dist > 0:
                    size = (self.equity * 0.02) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.sell(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.lowest = self.data.Low[-1]
                        print(f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨📉")

        # Exit logic
        # 🌙 Moon Dev Optimization: Removed RSI and EMA exits to let winners run longer in trends (only trailing stop)
        # Tightened trailing distance to 1.5 ATR (was 2) for better protection without early exits
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[-1])
                new_trail = self.highest - 1.5 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                if self.data.Low[-1] <= self.trail_sl:
                    self.position.close()
                    print(f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: Trailing Stop 💥")
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[-1])
                new_trail = self.lowest + 1.5 * self.atr[-1]
                self.trail_sl = min(self.trail_sl, new_trail)
                if self.data.High[-1] >= self.trail_sl:
                    self.position.close()
                    print(f"🌙 Moon Dev Short Exit at {self.data.Close[-1]:.2f} - Reason: Trailing Stop 💥")


# Run backtest
bt = Backtest(data, ExtremeDivergence, cash=1000000, commission=0.001, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
