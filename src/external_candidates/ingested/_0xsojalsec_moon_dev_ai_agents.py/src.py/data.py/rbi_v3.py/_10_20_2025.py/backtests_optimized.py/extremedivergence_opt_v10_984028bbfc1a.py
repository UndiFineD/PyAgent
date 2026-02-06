# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v10.py
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
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter to ensure entries in trending markets
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # 🌙 Moon Dev Optimization: Added volume SMA for confirmation to avoid low-volume fakeouts
        self.avg_volume = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0
        # 🌙 Moon Dev Optimization: Track initial risk for dynamic TP at 1:3 RR to lock in profits
        self.initial_risk = 0.0

    def next(self):
        # 🌙 Moon Dev Optimization: Skip early bars without sufficient history for reliable signals
        if len(self.data) < 250:
            return
        # Compute trend with longer slope period for stronger trend confirmation
        ema_slope = self.ema200[-1] - self.ema200[-21]
        uptrend = self.data.Close[-1] > self.ema200[-1] and ema_slope > 0
        downtrend = self.data.Close[-1] < self.ema200[-1] and ema_slope < 0

        # 🌙 Moon Dev Optimization: Limit divergence detection to recent 100 bars for fresher, more relevant signals
        slice_len = min(100, len(self.data.Close))
        # Compute bullish hidden divergence
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[-slice_len:].values
        low_indices = argrelextrema(price_slice_low, np.less_equal, order=3)[
            0
        ]  # Reduced order for more sensitive swing detection
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                hist_idx1 = len(self.hist) - slice_len + idx1
                hist_idx2 = len(self.hist) - slice_len + idx2
                h1 = self.hist.iloc[hist_idx1]
                h2 = self.hist.iloc[hist_idx2]
                if p2 > p1 and h2 < h1:
                    bullish_div = True
                    recent_swing_low = p2

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[-slice_len:].values
        high_indices = argrelextrema(price_slice_high, np.greater_equal, order=3)[
            0
        ]  # Reduced order for more sensitive swing detection
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            if idx2 - idx1 >= 5:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                hist_idx1 = len(self.hist) - slice_len + idx1
                hist_idx2 = len(self.hist) - slice_len + idx2
                h1 = self.hist.iloc[hist_idx1]
                h2 = self.hist.iloc[hist_idx2]
                if p2 < p1 and h2 > h1:
                    bearish_div = True
                    recent_swing_high = p2

        # Entry logic
        if not self.position:
            if (
                uptrend
                and bullish_div
                and self.rsi[-1] < 30
                and
                # 🌙 Moon Dev Optimization: ADX filter for strong trend, volume confirmation for quality setups
                self.adx[-1] > 25
                and self.data.Volume[-1] > self.avg_volume[-1]
            ):
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_low - 1.5 * atr_val
                risk_dist = entry - sl
                if risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk to 2% for higher potential returns, use float size for precision
                    size = self.equity * 0.02 / risk_dist
                    if size > 0:
                        self.buy(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.initial_risk = risk_dist  # Set for TP calculation
                        self.highest = self.data.High[-1]
                        print(
                            f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨🚀"
                        )
            elif (
                downtrend
                and bearish_div
                and self.rsi[-1] > 70
                and self.adx[-1] > 25
                and self.data.Volume[-1] > self.avg_volume[-1]
            ):
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_high + 1.5 * atr_val
                risk_dist = sl - entry
                if risk_dist > 0:
                    size = self.equity * 0.02 / risk_dist
                    if size > 0:
                        self.sell(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.initial_risk = risk_dist  # Set for TP calculation
                        self.lowest = self.data.Low[-1]
                        print(
                            f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨📉"
                        )

        # Exit logic
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[-1])
                new_trail = self.highest - 2 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                exit_reason = None
                # 🌙 Moon Dev Optimization: Prioritize TP at 1:3 RR before other exits to capture gains
                if self.data.Close[-1] > self.entry_price + 3 * self.initial_risk:
                    exit_reason = "Take Profit 1:3"
                elif self.data.Low[-1] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] > 70:
                    exit_reason = "RSI Overbought"
                elif self.data.Close[-1] < self.ema200[-1]:
                    exit_reason = "EMA Cross Below"
                if exit_reason:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥"
                    )
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[-1])
                new_trail = self.lowest + 2 * self.atr[-1]
                self.trail_sl = min(self.trail_sl, new_trail)
                exit_reason = None
                # 🌙 Moon Dev Optimization: Prioritize TP at 1:3 RR before other exits to capture gains
                if self.data.Close[-1] < self.entry_price - 3 * self.initial_risk:
                    exit_reason = "Take Profit 1:3"
                elif self.data.High[-1] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] < 30:
                    exit_reason = "RSI Oversold"
                elif self.data.Close[-1] > self.ema200[-1]:
                    exit_reason = "EMA Cross Above"
                if exit_reason:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Short Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥"
                    )


# Run backtest
bt = Backtest(
    data, ExtremeDivergence, cash=1000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
print(stats._strategy)
