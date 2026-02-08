# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v12.py
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
    lookback = 20
    recent_period = 10
    stoch_window = 5
    risk_pct = 0.02  # Optimized: Increased risk per trade to 2% for higher potential returns while managing drawdown
    rr = 3  # Optimized: Increased reward:risk to 3:1 to capture larger moves in volatile BTC
    max_bars = 30  # Optimized: Extended max hold time to 30 bars to allow more room for trends
    atr_mult_sl = 2.0  # Optimized: ATR multiplier for trailing stop to protect profits dynamically
    buffer_mult = 0.3  # Optimized: Tightened initial SL buffer for better risk-reward
    min_div_strength = 3  # Optimized: Added minimum RSI divergence strength to filter weak signals
    adx_min = 20  # Optimized: ADX threshold for trend strength filter to avoid choppy markets
    rsi_oversold = 40  # Optimized: Adjusted RSI oversold level for divergence to catch deeper setups
    stoch_oversold = 30  # Optimized: Raised stochastic oversold threshold to generate more convergence signals

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
        self.sma50 = self.I(
            talib.SMA, self.data.Close, timeperiod=50
        )  # Optimized: Switched to SMA50 from SMA200 for more responsive trend filter and more trade opportunities in uptrends
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )  # Optimized: Added ADX for market regime filter to ensure trending conditions
        self.vol_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=20
        )  # Optimized: Added volume SMA for confirmation filter to avoid low-volume false signals
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low = None
        self.div_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if (
            len(self.data) < 100
        ):  # Optimized: Reduced min bars required to 100 for faster initialization while covering indicators
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation) - Optimized: Tightened criteria with oversold filter and min strength for higher quality setups
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
            (low2 < low1)
            and (rsi2 > rsi1)
            and (rsi2 < self.rsi_oversold)
            and (rsi1 < self.rsi_oversold + 10)
            and (rsi2 - rsi1 > self.min_div_strength)
            and (distance <= 5)
        )
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence - Optimized: Adjusted oversold level for more frequent but still quality convergence signals
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (k_now < self.stoch_oversold) and (k_now > k_prev) and (gap_now < gap_prev) and (k_now < d_now)
        if stoch_converge:
            print(f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙")

        # Entry Logic - Optimized: Added ADX and volume filters for better entry quality; switched to SMA50
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma50[-1]
            and self.adx[-1] > self.adx_min
            and self.data.Volume[-1] > self.vol_sma[-1]
        ):
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
                # Optimized: Removed fixed TP to allow winners to run with trailing stop instead
                self.buy(size=size, sl=sl_price)
                self.entry_price = entry_price
                self.sl_price = sl_price
                # self.tp_price = entry_price + self.rr * risk_per_unit  # No longer used
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, SL: {sl_price} 🚀✨")
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic - Optimized: Added trailing stop and SMA50 breach exit; removed RSI>70 to avoid premature exits; kept stochastic cross for momentum reversal
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])

            # Optimized: Trailing stop to lock in profits dynamically based on ATR
            potential_sl = current_price - (self.atr[-1] * self.atr_mult_sl)
            if potential_sl > self.sl_price:
                self.sl_price = potential_sl
                self.position.sl = self.sl_price
                print(f"🌙 Moon Dev: Trailing SL updated to {self.sl_price} 🌙")

            # Optimized: Added trend filter exit if price falls below SMA50
            if current_price < self.sma50[-1]:
                self.position.close()
                print(f"🌙 Moon Dev: Price below SMA50! EXIT 📉")
                return

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
            # Removed: RSI >70 exit to let positions run longer in strong trends

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]} ✨"
            )


# Run backtest
bt = Backtest(data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
