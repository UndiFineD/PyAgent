# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v6.py
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
        macd_line, signal_line, hist = self.I(talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.hist = hist
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter to avoid choppy markets
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.entry_price = 0
        self.trail_sl = 0
        self.tp = 0  # 🌙 Moon Dev Optimization: Added take profit level for 3:1 RR
        self.highest = 0
        self.lowest = 0

    def next(self):
        current_len = len(self.ema200)
        if current_len < 21:  # 🌙 Moon Dev Optimization: Increased from 11 to 21 for more stable EMA slope calculation
            return
        # Compute trend with ADX filter
        ema_slope = self.ema200[-1] - self.ema200[-21]
        uptrend = self.data.Close[-1] > self.ema200[-1] and ema_slope > 0 and self.adx[-1] > 20
        downtrend = self.data.Close[-1] < self.ema200[-1] and ema_slope < 0 and self.adx[-1] > 20

        # 🌙 Moon Dev Optimization: Limited lookback to recent 100 bars for more relevant divergences, increased order to 7 for clearer swing detection
        lookback = min(100, current_len)
        # Compute bullish hidden divergence
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[-lookback:].values
        low_rel_indices = argrelextrema(price_slice_low, np.less_equal, order=7)[0]
        if len(low_rel_indices) >= 2:
            idx1 = low_rel_indices[-2]
            idx2 = low_rel_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                h1 = self.hist[-lookback + idx1]
                h2 = self.hist[-lookback + idx2]
                if p2 > p1 and h2 < h1:
                    # 🌙 Moon Dev Optimization: Added histogram turning filter for momentum confirmation
                    if self.hist[-1] > self.hist[-2]:
                        bullish_div = True
                        recent_swing_low = p2

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[-lookback:].values
        high_rel_indices = argrelextrema(price_slice_high, np.greater_equal, order=7)[0]
        if len(high_rel_indices) >= 2:
            idx1 = high_rel_indices[-2]
            idx2 = high_rel_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                h1 = self.hist[-lookback + idx1]
                h2 = self.hist[-lookback + idx2]
                if p2 < p1 and h2 > h1:
                    # 🌙 Moon Dev Optimization: Added histogram turning filter for momentum confirmation
                    if self.hist[-1] < self.hist[-2]:
                        bearish_div = True
                        recent_swing_high = p2

        # Entry logic with optimizations
        if not self.position:
            risk_percent = (
                0.02  # 🌙 Moon Dev Optimization: Increased risk from 1% to 2% for higher exposure and potential returns
            )
            # 🌙 Moon Dev Optimization: Loosened RSI thresholds to <40/>60 for more entry opportunities, added MACD line filter for trend alignment
            if uptrend and bullish_div and self.rsi[-1] < 40 and self.macd_line[-1] > 0:
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_low - 1.5 * atr_val
                risk_dist = entry - sl
                if risk_dist > 0:
                    size = (self.equity * risk_percent) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.buy(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.tp = entry + 3 * risk_dist  # 🌙 Moon Dev Optimization: Set 3:1 RR take profit
                        self.highest = self.data.High[-1]
                        print(
                            f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f}, TP: {self.tp:.2f} ✨🚀"
                        )
            elif downtrend and bearish_div and self.rsi[-1] > 60 and self.macd_line[-1] < 0:
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_high + 1.5 * atr_val
                risk_dist = sl - entry
                if risk_dist > 0:
                    size = (self.equity * risk_percent) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.sell(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.tp = entry - 3 * risk_dist  # 🌙 Moon Dev Optimization: Set 3:1 RR take profit
                        self.lowest = self.data.Low[-1]
                        print(
                            f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f}, TP: {self.tp:.2f} ✨📉"
                        )

        # Exit logic with optimizations
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[-1])
                # 🌙 Moon Dev Optimization: Tightened trailing stop to 1.5*ATR from 2*ATR for better profit locking
                new_trail = self.highest - 1.5 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                exit_reason = None
                if self.data.Low[-1] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.data.Close[-1] >= self.tp:
                    exit_reason = "Take Profit"  # 🌙 Moon Dev Optimization: Added TP exit
                elif self.rsi[-1] > 70:
                    exit_reason = "RSI Overbought"
                elif self.data.Close[-1] < self.ema200[-1]:
                    exit_reason = "EMA Cross Below"
                if exit_reason:
                    self.position.close()
                    print(f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[-1])
                # 🌙 Moon Dev Optimization: Tightened trailing stop to 1.5*ATR from 2*ATR for better profit locking
                new_trail = self.lowest + 1.5 * self.atr[-1]
                self.trail_sl = min(self.trail_sl, new_trail)
                exit_reason = None
                if self.data.High[-1] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.data.Close[-1] <= self.tp:
                    exit_reason = "Take Profit"  # 🌙 Moon Dev Optimization: Added TP exit
                elif self.rsi[-1] < 30:
                    exit_reason = "RSI Oversold"
                elif self.data.Close[-1] > self.ema200[-1]:
                    exit_reason = "EMA Cross Above"
                if exit_reason:
                    self.position.close()
                    print(f"🌙 Moon Dev Short Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")


# Run backtest
bt = Backtest(data, ExtremeDivergence, cash=1000000, commission=0.001, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
