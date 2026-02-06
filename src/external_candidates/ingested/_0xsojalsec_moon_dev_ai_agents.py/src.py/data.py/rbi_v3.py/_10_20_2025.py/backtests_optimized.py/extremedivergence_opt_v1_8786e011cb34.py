# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\ExtremeDivergence_OPT_v1.py
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
        # 🌙 Moon Dev Optimization: Changed EMA to 100 periods for more responsive trend detection on 15m timeframe
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=100)
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
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter (>20) to avoid choppy markets
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # 🌙 Moon Dev Optimization: Added volume SMA for confirmation of entries with increasing volume
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_price = 0
        self.trail_sl = 0
        self.highest = 0
        self.lowest = 0
        self.risk_dist = 0  # 🌙 Moon Dev Optimization: Track initial risk distance for 3R TP calculation

    def next(self):
        current_len = len(self.ema200)
        # 🌙 Moon Dev Optimization: Increased minimum length to 21 for stronger EMA slope over 20 periods
        if current_len < 21:
            return
        # Compute trend with enhanced slope and ADX filter
        # 🌙 Moon Dev Optimization: EMA slope over 20 periods for better trend confirmation
        ema_slope = self.ema200[-1] - self.ema200[-21]
        uptrend = (
            self.data.Close[-1] > self.ema200[-1]
            and ema_slope > 0
            and self.adx[-1] > 20
        )
        downtrend = (
            self.data.Close[-1] < self.ema200[-1]
            and ema_slope < 0
            and self.adx[-1] > 20
        )

        # Compute bullish hidden divergence with tighter swing detection
        bullish_div = False
        recent_swing_low = 0
        price_slice_low = self.data.Low[:current_len]
        # 🌙 Moon Dev Optimization: Increased order to 8 for more significant swing lows; min distance 8 bars
        low_indices = argrelextrema(price_slice_low, np.less_equal, order=8)[0]
        if len(low_indices) >= 2:
            idx1 = low_indices[-2]
            idx2 = low_indices[-1]
            if idx2 - idx1 >= 8:
                p1 = price_slice_low[idx1]
                p2 = price_slice_low[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 > p1 and h2 < h1:
                    bullish_div = True
                    recent_swing_low = p2

        # Compute bearish hidden divergence with tighter swing detection
        bearish_div = False
        recent_swing_high = 0
        price_slice_high = self.data.High[:current_len]
        # 🌙 Moon Dev Optimization: Increased order to 8 for more significant swing highs; min distance 8 bars
        high_indices = argrelextrema(price_slice_high, np.greater_equal, order=8)[0]
        if len(high_indices) >= 2:
            idx1 = high_indices[-2]
            idx2 = high_indices[-1]
            if idx2 - idx1 >= 8:
                p1 = price_slice_high[idx1]
                p2 = price_slice_high[idx2]
                h1 = self.hist[idx1]
                h2 = self.hist[idx2]
                if p2 < p1 and h2 > h1:
                    bearish_div = True
                    recent_swing_high = p2

        # Entry logic with optimized filters
        if not self.position:
            if (
                uptrend
                and bullish_div
                and self.rsi[-1] < 40
                and self.data.Volume[-1] > self.vol_sma[-1]
            ):
                # 🌙 Moon Dev Optimization: Loosened RSI to <40 for more entry opportunities; added volume filter
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                # 🌙 Moon Dev Optimization: Tightened initial SL to 1x ATR below swing low for better risk-reward and larger position sizes
                sl = recent_swing_low - atr_val
                risk_dist = entry - sl
                if risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk per trade to 2% equity for higher potential returns
                    size = (self.equity * 0.02) / risk_dist
                    size = int(
                        round(size)
                    )  # Keep as int for consistency, but allows scaling with equity
                    if size > 0:
                        self.buy(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.risk_dist = risk_dist  # Store for TP
                        self.highest = self.data.High[-1]
                        print(
                            f"🌙 Moon Dev Long Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨🚀"
                        )
            elif (
                downtrend
                and bearish_div
                and self.rsi[-1] > 60
                and self.data.Volume[-1] > self.vol_sma[-1]
            ):
                # 🌙 Moon Dev Optimization: Loosened RSI to >60 for more entry opportunities; added volume filter
                entry = self.data.Close[-1]
                atr_val = self.atr[-1]
                # 🌙 Moon Dev Optimization: Tightened initial SL to 1x ATR above swing high
                sl = recent_swing_high + atr_val
                risk_dist = sl - entry
                if risk_dist > 0:
                    # 🌙 Moon Dev Optimization: Increased risk per trade to 2% equity
                    size = (self.equity * 0.02) / risk_dist
                    size = int(round(size))
                    if size > 0:
                        self.sell(size=size)
                        self.entry_price = entry
                        self.trail_sl = sl
                        self.risk_dist = risk_dist  # Store for TP
                        self.lowest = self.data.Low[-1]
                        print(
                            f"🌙 Moon Dev Short Entry at {entry:.2f}! Size: {size}, SL: {sl:.2f} ✨📉"
                        )

        # Exit logic with prioritized checks and TP
        if self.position:
            exit_reason = None
            if self.position.is_long:
                # Update trailing high
                self.highest = max(self.highest, self.data.High[-1])
                # 🌙 Moon Dev Optimization: Adjusted trailing stop to 2x ATR to let winners run while protecting gains
                new_trail = self.highest - 2 * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
                # Prioritized exit checks
                # 🌙 Moon Dev Optimization: Added 3R Take Profit first for improved risk-reward
                profit = self.data.Close[-1] - self.entry_price
                if profit >= 3 * self.risk_dist:
                    exit_reason = "TP 3R"
                elif self.data.Low[-1] <= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] > 80:
                    # 🌙 Moon Dev Optimization: Loosened RSI exit to >80 to allow more room for profits
                    exit_reason = "RSI Overbought"
                elif self.data.Close[-1] < self.ema200[-1]:
                    exit_reason = "EMA Cross Below"
                if exit_reason:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long Exit at {self.data.Close[-1]:.2f} - Reason: {exit_reason} 💥"
                    )
            else:  # short
                # Update trailing low
                self.lowest = min(self.lowest, self.data.Low[-1])
                # 🌙 Moon Dev Optimization: Adjusted trailing stop to 2x ATR
                new_trail = self.lowest + 2 * self.atr[-1]
                self.trail_sl = min(self.trail_sl, new_trail)
                # Prioritized exit checks
                # 🌙 Moon Dev Optimization: Added 3R Take Profit
                profit = self.entry_price - self.data.Close[-1]
                if profit >= 3 * self.risk_dist:
                    exit_reason = "TP 3R"
                elif self.data.High[-1] >= self.trail_sl:
                    exit_reason = "Trailing Stop"
                elif self.rsi[-1] < 20:
                    # 🌙 Moon Dev Optimization: Loosened RSI exit to <20
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
