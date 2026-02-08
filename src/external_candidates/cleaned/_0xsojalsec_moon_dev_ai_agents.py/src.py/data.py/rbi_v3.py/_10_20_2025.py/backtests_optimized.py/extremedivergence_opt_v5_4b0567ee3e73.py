# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v5.py
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
        # 🌙 Moon Dev Optimization: Shortened EMA to 100 for faster trend detection on 15m timeframe, better responsiveness in crypto volatility
        self.ema100 = self.I(talib.EMA, self.data.Close, timeperiod=100)
        macd_line, signal_line, hist = self.I(talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.hist = hist
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        # 🌙 Moon Dev Optimization: Added volume SMA for filter to ensure entries on above-average volume, avoiding low-conviction setups
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0
        self.tp_level = 0  # For take profit
        self.risk_dist = 0  # To track risk for TP calculation

    def next(self):
        current_len = len(self.ema100)
        if current_len < 11:
            return
        # Compute trend with shorter EMA and slope
        ema_slope = self.ema100[-1] - self.ema100[-11]
        uptrend = self.data.Close[-1] > self.ema100[-1] and ema_slope > 0
        downtrend = self.data.Close[-1] < self.ema100[-1] and ema_slope < 0

        # 🌙 Moon Dev Optimization: Added volume filter (current volume > 1.2 * SMA20) to enter only on higher conviction moves
        volume_filter = self.data.Volume[-1] > 1.2 * self.volume_sma[-1]

        # Compute bullish hidden divergence
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[:current_len]
        low_indices = argrelextrema(price_slice_low, np.less_equal, order=5)[0]
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            # 🌙 Moon Dev Optimization: Increased min distance to 10 bars for more reliable divergences, reducing noise
            if idx2 - idx1 >= 10:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 > p1 and h2 < h1:
                    # 🌙 Moon Dev Optimization: Added momentum confirmation - recent hist turning up for bullish continuation
                    if self.hist[-1] > self.hist[-2]:
                        bullish_div = True
                        recent_swing_low = p2

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[:current_len]
        high_indices = argrelextrema(price_slice_high, np.greater_equal, order=5)[0]
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            # 🌙 Moon Dev Optimization: Increased min distance to 10 bars for more reliable divergences
            if idx2 - idx1 >= 10:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 < p1 and h2 > h1:
                    # 🌙 Moon Dev Optimization: Added momentum confirmation - recent hist turning down for bearish continuation
                    if self.hist[-1] < self.hist[-2]:
                        bearish_div = True
                        recent_swing_high = p2

        # Entry logic
        if not self.position:
            # 🌙 Moon Dev Optimization: Relaxed RSI to <40/>60 for more entry opportunities in pullbacks/throwovers, while keeping trend filter
            if uptrend and bullish_div and self.rsi[-1] < 40 and volume_filter:
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_low - 1.5 * atr_val
                self.risk_dist = entry - sl
                if self.risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk per trade to 2% for higher returns, balanced with better filters
                    size = (self.equity * 0.02) / self.risk_dist
                    size = max(0.01, min(1.0, size))  # Fraction 0-1, avoid zero or >1
                    self.buy(size=size)
                    self.entry_price = entry
                    self.trail_sl = sl
                    # 🌙 Moon Dev Optimization: Added 3:1 RR take profit for scaling out/profit locking
                    self.tp_level = entry + 3 * self.risk_dist
                    self.highest = self.data.High[-1]
                    print(
                        f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size:.4f}, SL: {sl:.2f}, TP: {self.tp_level:.2f} ✨🚀"
                    )
            elif downtrend and bearish_div and self.rsi[-1] > 60 and volume_filter:
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_high + 1.5 * atr_val
                self.risk_dist = sl - entry
                if self.risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk per trade to 2%
                    size = (self.equity * 0.02) / self.risk_dist
                    size = max(0.01, min(1.0, size))
                    self.sell(size=size)
                    self.entry_price = entry
                    self.trail_sl = sl
                    # 🌙 Moon Dev Optimization: Added 3:1 RR take profit
                    self.tp_level = entry - 3 * self.risk_dist
                    self.lowest = self.data.Low[-1]
                    print(
                        f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size:.4f}, SL: {sl:.2f}, TP: {self.tp_level:.2f} ✨📉"
                    )

        # Exit logic
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[-1])
                # 🌙 Moon Dev Optimization: Tightened trailing to 1.5 ATR for better profit capture in volatile BTC
                new_trail = self.highest - 1.5 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                exit_reason = None
                # 🌙 Moon Dev Optimization: Added TP check before other exits
                if self.data.High[-1] >= self.tp_level:
                    exit_reason = "Take Profit"
                    self.position.close()
                    print(f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")
                    return
                if self.data.Low[-1] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] > 70:
                    exit_reason = "RSI Overbought"
                elif self.data.Close[-1] < self.ema100[-1]:
                    exit_reason = "EMA Cross Below"
                if exit_reason:
                    self.position.close()
                    print(f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[-1])
                # 🌙 Moon Dev Optimization: Tightened trailing to 1.5 ATR
                new_trail = self.lowest + 1.5 * self.atr[-1]
                self.trail_sl = min(self.trail_sl, new_trail)
                exit_reason = None
                # 🌙 Moon Dev Optimization: Added TP check
                if self.data.Low[-1] <= self.tp_level:
                    exit_reason = "Take Profit"
                    self.position.close()
                    print(f"🌙 Moon Dev Short Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")
                    return
                if self.data.High[-1] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] < 30:
                    exit_reason = "RSI Oversold"
                elif self.data.Close[-1] > self.ema100[-1]:
                    exit_reason = "EMA Cross Above"
                if exit_reason:
                    self.position.close()
                    print(f"🌙 Moon Dev Short Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥")


# Run backtest
bt = Backtest(data, ExtremeDivergence, cash=1000000, commission=0.001, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
