# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v8.py
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
    lookback = 15  # Reduced from 20 to detect divergences more frequently for more entry opportunities 🌙
    recent_period = 8  # Reduced from 10 to tighten recent low detection, improving signal quality ✨
    stoch_window = 5
    risk_pct = 0.02  # Increased from 0.01 to 2% risk per trade for higher exposure and potential returns, balanced with volatility sizing 🚀
    rr = 3  # Increased from 2 to 3 for better reward-to-risk ratio, aiming for higher profitability per trade 🌙
    max_bars = 20  # Increased from 15 to allow positions more time to develop in volatile BTC 15m, reducing premature time exits ✨
    atr_mult_sl = 1.5  # Added ATR multiplier for SL placement below (was implicit)
    buffer_mult = 0.5
    trail_atr_mult = 2.0  # New: ATR multiplier for trailing stop activation and distance 🌙
    trail_start_rr = 1.0  # New: Start trailing after 1:1 RR profit to lock in gains early 🚀

    def init(self):
        self.rsi = self.I(
            talib.RSI, self.data.Close, timeperiod=10
        )  # Shortened from 14 to 10 for more sensitive oversold signals in short-term BTC moves ✨
        self.slowk = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, fastk_period=8, slowk_period=3, slowd_period=3)[0],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )  # Faster Stoch from 14 to 8 for quicker convergence detection 🌙
        self.slowd = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, fastk_period=8, slowk_period=3, slowd_period=3)[1],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.ema50 = self.I(
            talib.EMA, self.data.Close, timeperiod=50
        )  # Changed from SMA200 to EMA50 for more responsive trend filter in 15m timeframe, catching uptrends sooner 🚀
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.volume_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=20
        )  # New: Volume SMA for confirmation filter to avoid low-volume fakeouts ✨
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.trail_sl = None  # New: For trailing stop management 🌙
        self.div_low = None
        self.div_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < 100:  # Reduced from 220 since using EMA50 instead of SMA200, faster initialization ✨
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1
        current_volume = self.data.Volume[-1]
        vol_sma = self.volume_sma[-1]

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation) - Added volume filter for recent low
        lows_older = self.data.Low[-self.lookback : -self.recent_period]
        rsi_older = self.rsi[-self.lookback : -self.recent_period]
        argmin_low_older = np.argmin(lows_older)
        low1 = lows_older[argmin_low_older]
        rsi1 = rsi_older[argmin_low_older]
        lows_recent_part = self.data.Low[-self.recent_period :]
        rsi_recent_part = self.rsi[-self.recent_period :]
        volumes_recent = self.data.Volume[-self.recent_period :]
        argmin_low_recent = np.argmin(lows_recent_part)
        low2 = lows_recent_part[argmin_low_recent]
        rsi2 = rsi_recent_part[argmin_low_recent]
        vol_at_recent_low = volumes_recent[argmin_low_recent]  # New: Volume at recent low
        distance = self.recent_period - 1 - argmin_low_recent

        # Tightened bull_div: Added RSI divergence strength threshold and volume > SMA for quality filter 🌙
        bull_div = (
            (low2 < low1) and (rsi2 > rsi1 + 2) and (rsi2 < 50) and (distance <= 5) and (vol_at_recent_low > vol_sma)
        )
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars, Volume confirmed!"
            )

        # Stochastic Convergence - Added momentum filter: %K increasing over window
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        # New: Ensure %K is rising over the window for stronger momentum 🚀
        k_momentum = k_now > self.slowk[-self.stoch_window * 2] if len(self.slowk) >= self.stoch_window * 2 else True
        stoch_converge = (k_now < 20) and (k_now > k_prev) and (gap_now < gap_prev) and (k_now < d_now) and k_momentum
        if stoch_converge:
            print(
                f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! Momentum: {k_momentum} 🌙"
            )

        # Entry Logic - Updated trend filter to EMA50, added volatility-based size adjustment
        if not self.position and self.div_bar is not None and stoch_converge and current_price > self.ema50[-1]:
            print(f"🌙 Moon Dev: All entry conditions met! Attempting LONG entry... 🚀")
            # Calculate SL: below div low with ATR buffer, now using atr_mult_sl
            div_low = self.div_low
            atr_val = self.atr[-1]
            sl_price = div_low - (
                atr_val * self.atr_mult_sl
            )  # Improved SL placement with explicit ATR mult for better risk management ✨
            entry_price = current_price
            risk_per_unit = entry_price - sl_price
            if risk_per_unit <= 0:
                print(f"🌙 Moon Dev: Invalid risk per unit: {risk_per_unit}, skipping entry. ⚠️")
                return
            # Dynamic sizing: Scale risk_pct down if ATR high (volatility filter) to maintain good risk management 🌙
            vol_adjust = min(1.0, 0.02 / (atr_val / entry_price))  # Cap exposure in high vol
            size_frac = (self.risk_pct * vol_adjust) * entry_price / risk_per_unit
            size = min(1.0, size_frac)
            if size > 0:
                tp_price = entry_price + self.rr * risk_per_unit
                self.buy(size=size, sl=sl_price, tp=tp_price)
                self.entry_price = entry_price
                self.sl_price = sl_price
                self.tp_price = tp_price
                self.trail_sl = sl_price  # Initialize trailing SL 🌙
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction, vol-adjusted), Entry: {entry_price}, SL: {sl_price}, TP: {tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic - Added trailing stop logic
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])

            # New: Trailing Stop - Activate after trail_start_rr profit, trail with ATR
            profit_rr = (
                (current_price - self.entry_price) / (self.entry_price - self.sl_price)
                if (self.entry_price - self.sl_price) > 0
                else 0
            )
            if profit_rr >= self.trail_start_rr:
                new_trail = current_price - (self.atr[-1] * self.trail_atr_mult)
                self.trail_sl = max(self.trail_sl, new_trail)
                self.position.sl = self.trail_sl  # Update SL to trail 🚀
                print(f"🌙 Moon Dev: Trailing SL updated to {self.trail_sl} (RR: {profit_rr:.2f}) ✨")

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                return

            # Dynamic exits
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                return
            if rsi_now > 70:
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >70! EXIT 📈")
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]} ✨"
            )


# Run backtest
bt = Backtest(data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
