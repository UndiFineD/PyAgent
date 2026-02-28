# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v11.py
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
print(
    "🌙 Moon Dev: Data loaded and cleaned successfully! Columns: Open, High, Low, Close, Volume. Index: Datetime. ✨"
)


class DivergentConvergence(Strategy):
    pivot_window = 5  # Not used, using approximation
    lookback = 25  # Increased for better historical low detection 🌙
    recent_period = 12  # Adjusted for optimal recent low capture ✨
    stoch_window = 8  # Fine-tuned for stochastic signal reliability 🚀
    risk_pct = 0.01  # Kept conservative for risk management
    rr = 2.5  # Increased RR for higher reward potential while balanced 📈
    max_bars = 20  # Extended hold time to allow trends to develop 🌙
    atr_mult_sl = 2.0  # Used for trailing stop distance
    buffer_mult = (
        1.0  # Increased buffer for more realistic SL placement below div low ⚠️
    )
    adx_threshold = 20  # Added ADX threshold to filter for trending markets only 📊
    trail_mult = 2.0  # Trailing stop multiplier for profit locking ✨

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.slowk = self.I(
            lambda h, l, c: talib.STOCH(
                h, l, c, fastk_period=14, slowk_period=3, slowd_period=3
            )[0],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.slowd = self.I(
            lambda h, l, c: talib.STOCH(
                h, l, c, fastk_period=14, slowk_period=3, slowd_period=3
            )[1],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # Added complementary indicators for optimization 🌙
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.trail_sl = None  # Added for trailing stop management 🚀
        self.div_low = None
        self.div_bar = None
        print(
            "🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators including ADX and Volume SMA... 🚀"
        )

    def reset_pos_vars(self):
        """Helper to reset position variables on exit 🌙"""
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.trail_sl = None

    def next(self):
        if (
            len(self.data) < 250
        ):  # Increased buffer for all indicators including ADX/SMA200
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation) - Tightened for stronger signals
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

        # Optimized bull_div: Added minimum divergence strength and deeper oversold, looser distance
        bull_div = (
            (low2 < low1) and (rsi2 > rsi1 + 3) and (rsi2 < 45) and (distance <= 8)
        )
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence - Adjusted threshold for earlier detection
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (
            (k_now < 25)
            and (k_now > k_prev)
            and (gap_now < gap_prev)
            and (k_now < d_now)
        )
        if stoch_converge:
            print(
                f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙"
            )

        # Entry Logic - Added ADX and Volume filters for higher quality setups 📊
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and self.adx[-1] > self.adx_threshold
            and self.data.Volume[-1] > self.vol_sma[-1]
        ):
            print(f"🌙 Moon Dev: All entry conditions met! Attempting LONG entry... 🚀")
            # Calculate SL: below div low with increased buffer for better risk management
            div_low = self.div_low
            atr_val = self.atr[-1]
            sl_price = div_low - (atr_val * self.buffer_mult)
            entry_price = current_price
            risk_per_unit = entry_price - sl_price
            if risk_per_unit <= 0:
                print(
                    f"🌙 Moon Dev: Invalid risk per unit: {risk_per_unit}, skipping entry. ⚠️"
                )
                return
            size_frac = self.risk_pct * entry_price / risk_per_unit
            size = min(1.0, size_frac)
            if size > 0:
                tp_price = entry_price + self.rr * risk_per_unit
                # Enter without fixed SL/TP for dynamic trailing management ✨
                self.buy(size=size)
                self.entry_price = entry_price
                self.sl_price = sl_price
                self.tp_price = tp_price
                self.trail_sl = sl_price  # Initialize trailing SL
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, SL: {sl_price}, TP: {tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic - Now manual with trailing stop for better profit capture 📈
        if self.position:
            bars_held = (
                current_bar - self.entry_bar if self.entry_bar is not None else 0
            )
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (
                self.slowk[-1] < self.slowd[-1]
            )
            atr_val = self.atr[-1]

            # Update trailing stop if in profit - Starts after 1 ATR gain, trails by trail_mult ATR 🌙
            if bars_held >= 2 and current_price > self.entry_price + atr_val * 1.0:
                new_trail_sl = current_price - atr_val * self.trail_mult
                self.trail_sl = max(self.trail_sl, new_trail_sl)
                print(f"🌙 Moon Dev: Trailing SL updated to {self.trail_sl} 📊")

            # Trailing SL exit
            if current_price <= self.trail_sl:
                self.position.close()
                print(f"🌙 Moon Dev: Trailing Stop Hit! EXIT 📉")
                self.reset_pos_vars()
                return

            # Take Profit exit
            if current_price >= self.tp_price:
                self.position.close()
                print(f"🌙 Moon Dev: Take Profit Hit! EXIT 💰")
                self.reset_pos_vars()
                return

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                self.reset_pos_vars()
                return

            # Dynamic exits
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                self.reset_pos_vars()
                return
            if rsi_now > 70:
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >70! EXIT 📈")
                self.reset_pos_vars()
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]}, Trail SL: {self.trail_sl} ✨"
            )


# Run backtest
bt = Backtest(
    data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True
)
stats = bt.run()
print(stats)
