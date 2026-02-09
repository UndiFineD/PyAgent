# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v3.py
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
        # 🌙 Moon Dev Optimization: Fine-tuned MACD to 8-21-5 for faster signals on 15m, better for crypto volatility
        macd_line, signal_line, hist = self.I(
            talib.MACD, self.data.Close, fastperiod=8, slowperiod=21, signalperiod=5
        )
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.hist = hist
        # 🌙 Moon Dev Optimization: RSI period to 10 for quicker overbought/oversold detection
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=10)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter (>25 to avoid choppy markets)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # 🌙 Moon Dev Optimization: Volume SMA for confirmation (volume > 1.2x avg for entries)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0
        # 🌙 Moon Dev Optimization: Track for take profit (target 3:1 RR)
        self.initial_sl = 0
        self.tp_level = 0

    def next(self):
        current_len = len(self.ema200)
        if current_len < 11:
            return
        # Compute trend with slope over 11 periods (kept for smoothness)
        ema_slope = self.ema200[-1] - self.ema200[-11]
        uptrend = (
            self.data.Close[-1] > self.ema200[-1]
            and ema_slope > 0
            and self.adx[-1] > 25
        )  # Added ADX filter
        downtrend = (
            self.data.Close[-1] < self.ema200[-1]
            and ema_slope < 0
            and self.adx[-1] > 25
        )  # Added ADX filter

        # 🌙 Moon Dev Optimization: Limit divergence search to last 100 bars for more recent/relevant signals
        search_window = min(100, current_len)
        price_slice_low = self.data.Low[-search_window:current_len]
        low_indices_rel = argrelextrema(price_slice_low.values, np.less_equal, order=3)[
            0
        ]  # Tighter order=3 for more swings
        low_indices = (
            [i - search_window for i in low_indices_rel]
            if len(low_indices_rel) > 0
            else []
        )

        # Compute bullish hidden divergence
        bullish_div = False
        recent_swing_low = 0
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            if (
                current_len - idx2 <= 20 and idx2 - idx1 >= 3
            ):  # Ensure recent (within 20 bars) and min distance
                p1 = self.data.Low[idx1]
                p2 = self.data.Low[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 > p1 and h2 < h1:
                    bullish_div = True
                    recent_swing_low = p2

        price_slice_high = self.data.High[-search_window:current_len]
        high_indices_rel = argrelextrema(
            price_slice_high.values, np.greater_equal, order=3
        )[
            0
        ]  # Tighter order=3
        high_indices = (
            [i - search_window for i in high_indices_rel]
            if len(high_indices_rel) > 0
            else []
        )

        # Compute bearish hidden divergence
        bearish_div = False
        recent_swing_high = 0
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            if current_len - idx2 <= 20 and idx2 - idx1 >= 3:  # Recent and min distance
                p1 = self.data.High[idx1]
                p2 = self.data.High[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 < p1 and h2 > h1:
                    bearish_div = True
                    recent_swing_high = p2

        # 🌙 Moon Dev Optimization: Loosened RSI to <40/>60 for more entries, added volume >1.2x SMA
        vol_confirm = self.data.Volume[-1] > 1.2 * self.volume_sma[-1]

        # Entry logic
        if not self.position:
            if (
                uptrend and bullish_div and self.rsi[-1] < 40 and vol_confirm
            ):  # Loosened RSI, added volume
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = (
                    recent_swing_low - 1.2 * atr_val
                )  # Tighter initial SL multiplier for better RR
                risk_dist = entry - sl
                if risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk to 2% for higher returns (balances with better filters)
                    size = (self.equity * 0.02) / risk_dist
                    size = max(
                        0.01, min(1.0, size)
                    )  # Fraction for precision, cap at 100% equity
                    self.buy(size=size)
                    self.entry_price = entry
                    self.trail_sl = sl
                    self.initial_sl = sl
                    self.highest = self.data.High[-1]
                    # 🌙 Moon Dev Optimization: Added TP at 3x risk distance for scaling out potential
                    self.tp_level = entry + 3 * risk_dist
                    print(
                        f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size:.4f}, SL: {sl:.2f}, TP: {self.tp_level:.2f} ✨🚀"
                    )
            elif (
                downtrend and bearish_div and self.rsi[-1] > 60 and vol_confirm
            ):  # Loosened RSI, added volume
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl = recent_swing_high + 1.2 * atr_val  # Tighter initial SL
                risk_dist = sl - entry
                if risk_dist > 0:
                    # Increased to 2% risk
                    size = (self.equity * 0.02) / risk_dist
                    size = max(0.01, min(1.0, size))  # Fraction
                    self.sell(size=size)
                    self.entry_price = entry
                    self.trail_sl = sl
                    self.initial_sl = sl
                    self.lowest = self.data.Low[-1]
                    self.tp_level = entry - 3 * risk_dist
                    print(
                        f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size:.4f}, SL: {sl:.2f}, TP: {self.tp_level:.2f} ✨📉"
                    )

        # Exit logic
        if self.position:
            if self.position.is_long:
                self.highest = max(self.highest, self.data.High[-1])
                # 🌙 Moon Dev Optimization: Tighter trailing (1.5*ATR) to lock profits sooner
                new_trail = self.highest - 1.5 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                # 🌙 Moon Dev Optimization: Added TP hit check
                exit_reason = None
                if self.data.High[-1] >= self.tp_level:
                    exit_reason = "Take Profit Hit"
                    # Scale out: close 50% here, let rest trail
                    self.position.close(size=self.position.size * 0.5)
                    print(
                        f"🌙 Moon Dev Long Partial TP at {self.data.Close[-1]:.2f} - Scaled out 50% 💰"
                    )
                    return  # Don't fully close yet
                elif self.data.Low[-1] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] > 75:  # Tightened exit RSI for longs
                    exit_reason = "RSI Overbought"
                elif self.data.Close[-1] < self.ema200[-1]:
                    exit_reason = "EMA Cross Below"
                if exit_reason and self.position.size > 0:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥"
                    )
            else:  # short
                self.lowest = min(self.lowest, self.data.Low[-1])
                new_trail = self.lowest + 1.5 * self.atr[-1]  # Tighter trailing
                self.trail_sl = min(self.trail_sl, new_trail)
                exit_reason = None
                if self.data.Low[-1] <= self.tp_level:
                    exit_reason = "Take Profit Hit"
                    self.position.close(size=abs(self.position.size) * 0.5)
                    print(
                        f"🌙 Moon Dev Short Partial TP at {self.data.Close[-1]:.2f} - Scaled out 50% 💰"
                    )
                    return
                elif self.data.High[-1] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] < 25:  # Tightened exit RSI for shorts
                    exit_reason = "RSI Oversold"
                elif self.data.Close[-1] > self.ema200[-1]:
                    exit_reason = "EMA Cross Above"
                if exit_reason and abs(self.position.size) > 0:
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
