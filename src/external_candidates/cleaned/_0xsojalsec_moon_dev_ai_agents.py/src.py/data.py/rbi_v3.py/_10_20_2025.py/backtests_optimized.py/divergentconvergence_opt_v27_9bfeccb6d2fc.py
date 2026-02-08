# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v27.py
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
    lookback = 20  # 🌙 Moon Dev Optimization: Increased lookback to 20 for broader historical low comparison, improving divergence reliability without overfiltering
    recent_period = 6  # 🌙 Moon Dev Optimization: Reduced recent period to 6 for fresher recent lows, capturing more timely bullish setups in volatile 15m BTC
    stoch_window = 10  # 🌙 Moon Dev Optimization: Adjusted stochastic window to 10 for balanced smoothing, reducing false convergences while maintaining sensitivity
    risk_pct = 0.02  # 🌙 Moon Dev Optimization: Increased risk per trade to 2% to amplify returns on high-conviction signals, balanced with enhanced filters
    rr = 3.0  # 🌙 Moon Dev Optimization: Raised RR to 3:1 to target larger profit captures in trending BTC moves, improving overall expectancy
    max_bars = 40  # 🌙 Moon Dev Optimization: Extended max hold to 40 bars to allow sufficient trend development on 15m timeframe without excessive exposure
    atr_mult_sl = 1.8  # 🌙 Moon Dev Optimization: Fine-tuned ATR multiplier to 1.8 for a tighter yet forgiving trailing stop, locking profits more aggressively
    buffer_mult = 0.8  # 🌙 Moon Dev Optimization: Slightly reduced buffer to 0.8 for closer initial SL placement, minimizing risk on valid divergences

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
        # 🌙 Moon Dev Optimization: Added EMA20 as a short-term trend filter to ensure entries align with immediate uptrend momentum
        self.ema20 = self.I(talib.EMA, self.data.Close, timeperiod=20)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low = None
        self.div_bar = None
        self.current_sl = None  # 🌙 Moon Dev Optimization: Track current trailing SL level
        self.highest_since_entry = None  # 🌙 Moon Dev Optimization: Track highest high since entry for more accurate ATR-based trailing from peaks
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < 250:  # Enough for SMA200 + lookback + safety buffer
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1

        # Reset trade variables if no position
        if not self.position:
            self.current_sl = None
            self.highest_since_entry = None
            self.entry_bar = None
            self.entry_price = None
            self.sl_price = None
            self.tp_price = None

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
            (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 40) and (rsi1 < 50) and (distance <= 3)
        )  # 🌙 Moon Dev Optimization: Tightened RSI thresholds (<40 for recent, <50 for older) and distance (<=3) for higher-quality, deeper oversold divergences with minimal lag
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
        )  # 🌙 Moon Dev Optimization: Deepened %K threshold to <20 for stronger oversold convergence signals in BTC's volatile environment
        if stoch_converge:
            print(f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙")

        # Entry Logic
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and current_price > self.ema20[-1]
            and self.data.Volume[-1] > 1.5 * self.vol_sma[-1]
            and self.adx[-1] > 25
        ):  # 🌙 Moon Dev Optimization: Added EMA20 filter for short-term uptrend confirmation, raised volume threshold to 1.5x and ADX to >25 for elite high-volume, strong-trend entries only
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
                tp_price = entry_price + self.rr * risk_per_unit
                self.buy(
                    size=size, tp=tp_price
                )  # 🌙 Moon Dev Optimization: Removed fixed SL from order to enable manual trailing management
                self.entry_price = entry_price
                self.sl_price = sl_price
                self.tp_price = tp_price
                self.entry_bar = current_bar
                self.current_sl = sl_price  # 🌙 Moon Dev Optimization: Initialize trailing SL at entry SL level
                self.highest_since_entry = (
                    entry_price  # 🌙 Moon Dev Optimization: Initialize highest tracking at entry price
                )
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, Initial SL: {sl_price}, TP: {tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])

            # Update highest since entry
            if self.highest_since_entry is None:
                self.highest_since_entry = self.entry_price
            self.highest_since_entry = max(self.highest_since_entry, self.data.High[-1])

            # 🌙 Moon Dev Optimization: Update trailing SL dynamically every bar from highest high to better protect gains in uptrends
            if self.current_sl is None:
                self.current_sl = self.sl_price
            new_trail_sl = self.highest_since_entry - (self.atr[-1] * self.atr_mult_sl)
            self.current_sl = max(self.current_sl, new_trail_sl)

            # Trend filter exit
            if current_price < self.sma200[-1]:
                self.position.close()
                print(f"🌙 Moon Dev: Price below SMA200! Trend change EXIT 📉")
                self.current_sl = None
                self.highest_since_entry = None
                return

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                self.current_sl = None
                self.highest_since_entry = None
                return

            # Stochastic cross exit
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                self.current_sl = None
                self.highest_since_entry = None
                return

            # RSI overbought exit
            if rsi_now > 70:
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >70! EXIT 📈")
                self.current_sl = None
                self.highest_since_entry = None
                return

            # Trailing SL check
            if current_price < self.current_sl:
                self.position.close()
                print(f"🌙 Moon Dev: Trailing SL hit at {current_price}! 📉")
                self.current_sl = None
                self.highest_since_entry = None
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]}, Trail SL: {self.current_sl} ✨"
            )


# Run backtest
bt = Backtest(data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
