# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v29.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data loading and cleaning
path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "date": "datetime",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)
data = data.set_index(pd.to_datetime(data["datetime"])).drop(columns=["datetime"])
print("🌙 Moon Dev: Data loaded and cleaned successfully! Columns: Open, High, Low, Close, Volume. Index: Datetime. ✨")


class DivergentConvergence(Strategy):
    pivot_window = 5  # Not used, using approximation
    lookback = 12  # 🌙 Moon Dev Optimization: Reduced lookback slightly to focus on more recent divergences for timelier signals without losing robustness
    recent_period = 6  # 🌙 Moon Dev Optimization: Shortened recent period to capture fresher low comparisons, increasing signal frequency in volatile BTC
    stoch_window = (
        10  # 🌙 Moon Dev Optimization: Extended stochastic window for smoother and more reliable convergence detection
    )
    risk_pct = 0.02  # 🌙 Moon Dev Optimization: Increased risk per trade to 2% to amplify returns from winning trades while keeping per-trade risk controlled
    rr = 3.0  # 🌙 Moon Dev Optimization: Raised RR target to 3:1 as a reference for potential profit levels, though now used flexibly with partial exits and trailing
    max_bars = 40  # 🌙 Moon Dev Optimization: Extended max hold time to 40 bars to allow BTC trends more development time for higher reward capture
    atr_mult_sl = 1.8  # 🌙 Moon Dev Optimization: Adjusted ATR multiplier for trailing stop to a balanced level, tighter than before to lock profits sooner in chop
    buffer_mult = 0.8  # 🌙 Moon Dev Optimization: Slightly increased buffer for initial SL to provide a bit more room below divergence low, reducing wick-based stops

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.slowk = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, fastk_period=14, slowk_period=3, slowd_period=3)[0],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.slowd = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, fastk_period=14, slowk_period=3, slowd_period=3)[1],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        # 🌙 Moon Dev Optimization: Added volume SMA filter to enter only on above-average volume for higher conviction setups
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter to avoid choppy markets and focus on trending conditions
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low = None
        self.div_bar = None
        self.current_sl = None  # 🌙 Moon Dev Optimization: Track current trailing SL level
        self.entry_high = (
            None  # 🌙 Moon Dev Optimization: Track running high since entry for improved trailing stop from peaks
        )
        self.partial_taken = False  # 🌙 Moon Dev Optimization: Flag to track if partial profit has been taken
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < 220:  # Enough for SMA200 + lookback
            return

        current_price = self.data.Close[-1]
        current_high = self.data.High[-1]  # 🌙 Moon Dev Optimization: Use High for better trailing reference
        current_bar = len(self.data) - 1
        current_open = self.data.Open[-1]  # 🌙 Moon Dev Optimization: For bullish bar confirmation

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation)
        lows_older = self.data.Low[-self.lookback : -self.recent_period]
        rsi_older = self.rsi[-self.lookback : -self.recent_period]
        argmin_low_older = np.argmin(lows_older)
        low1 = lows_older[argmin_low_older]
        rsi1 = rsi_older[argmin_low_older]
        lows_recent_part = self.data.Low[-self.recent_period :]
        rsi_recent_part = self.rsi[-self.recent_period :]
        argmin_low_recent = np.argmin(lows_recent_part)
        low2 = lows_recent_part[argmin_low_recent]
        rsi2 = rsi_recent_part[argmin_low_recent]
        distance = self.recent_period - 1 - argmin_low_recent

        bull_div = (
            (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 40) and (distance <= 3)
        )  # 🌙 Moon Dev Optimization: Tightened RSI threshold to <40 for stronger oversold divergences and distance to <=3 for very fresh signals
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (
            (k_now < 20) and (k_now > k_prev) and (gap_now < gap_prev) and (k_now < d_now)
        )  # 🌙 Moon Dev Optimization: Lowered %K threshold to <20 to catch deeper oversold convergences in BTC's volatile swings
        if stoch_converge:
            print(f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙")

        # Entry Logic
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and self.data.Volume[-1] > 1.2 * self.vol_sma[-1]
            and self.adx[-1] > 22
            and current_price > current_open
        ):  # 🌙 Moon Dev Optimization: Strengthened volume filter to >1.2x SMA, raised ADX to >22 for stronger trends, added bullish bar (close>open) for momentum confirmation
            print(f"🌙 Moon Dev: All entry conditions met! Attempting LONG entry... 🚀")
            # Calculate SL: below div low with buffer
            div_low = self.div_low
            atr_val = self.atr[-1]
            sl_price = div_low - (atr_val * self.buffer_mult)
            entry_price = current_price
            risk_per_unit = entry_price - sl_price
            if risk_per_unit <= 0:
                print(f"🌙 Moon Dev: Invalid risk per unit: {risk_per_unit}, skipping entry. ⚠️")
                return
            size_frac = self.risk_pct * entry_price / risk_per_unit
            size = min(1.0, size_frac)
            if size > 0:
                # 🌙 Moon Dev Optimization: Removed fixed TP from buy order to enable full manual exit management with partial profits and dynamic trailing
                self.buy(size=size)
                self.entry_price = entry_price
                self.sl_price = sl_price
                self.tp_price = entry_price + self.rr * risk_per_unit  # Keep for reference but not used in order
                self.entry_bar = current_bar
                self.current_sl = sl_price  # 🌙 Moon Dev Optimization: Initialize trailing SL at entry SL level
                self.entry_high = entry_price  # 🌙 Moon Dev Optimization: Initialize running high for trailing
                self.partial_taken = False  # 🌙 Moon Dev Optimization: Reset partial flag for new position
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, Initial SL: {sl_price}, Target Ref: {self.tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])

            # 🌙 Moon Dev Optimization: Update running high and trailing SL from high for better profit locking during pullbacks
            if self.entry_high is None:
                self.entry_high = current_high
            else:
                self.entry_high = max(self.entry_high, current_high)
            new_trail_sl = self.entry_high - (self.atr[-1] * self.atr_mult_sl)
            self.current_sl = max(self.current_sl, new_trail_sl)

            # 🌙 Moon Dev Optimization: Partial profit taking at 1:1 RR to secure gains early, scaling out 50% while trailing the rest for higher potential
            risk_amount = self.entry_price - self.sl_price
            if not self.partial_taken and current_price >= self.entry_price + risk_amount:
                partial_size = self.position.size * 0.5
                self.sell(size=partial_size)
                self.partial_taken = True
                print(f"🌙 Moon Dev: Partial profit taken at 1:1 RR! Sold {partial_size:.4f} at {current_price} ✨")

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                self.current_sl = None
                self.entry_high = None
                self.partial_taken = False
                return

            # Stochastic cross exit
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                self.current_sl = None
                self.entry_high = None
                self.partial_taken = False
                return

            # RSI overbought exit
            if (
                rsi_now > 75
            ):  # 🌙 Moon Dev Optimization: Raised overbought threshold to 75 to hold positions longer in strong uptrends
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >75! EXIT 📈")
                self.current_sl = None
                self.entry_high = None
                self.partial_taken = False
                return

            # Trailing SL check
            if current_price < self.current_sl:
                self.position.close()
                print(f"🌙 Moon Dev: Trailing SL hit at {current_price}! 📉")
                self.current_sl = None
                self.entry_high = None
                self.partial_taken = False
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]}, Trail SL: {self.current_sl}, High: {self.entry_high} ✨"
            )


# Run backtest
bt = Backtest(data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
