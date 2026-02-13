# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v5.py
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
    lookback = 30  # Increased from 20 to capture better historical lows for divergence detection 🌙
    recent_period = 10
    stoch_window = (
        3  # Tightened from 5 for faster stochastic signals on 15m timeframe ✨
    )
    risk_pct = 0.01
    rr = 3  # Increased from 2 to aim for higher reward:risk, improving potential returns while managing risk 🚀
    max_bars = 20  # Extended from 15 to allow positions more time to develop in volatile BTC markets 🌙
    atr_mult_sl = 1.5
    buffer_mult = 0.5
    trail_mult = 1.5  # New: Multiplier for ATR-based trailing stop to lock in profits dynamically ✨

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        # Adjusted stochastic to faster periods for better responsiveness in short-term trades
        self.slowk = self.I(
            lambda h, l, c: talib.STOCH(
                h, l, c, fastk_period=8, slowk_period=3, slowd_period=3
            )[0],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.slowd = self.I(
            lambda h, l, c: talib.STOCH(
                h, l, c, fastk_period=8, slowk_period=3, slowd_period=3
            )[1],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)
        # New: EMA20 for short-term trend confirmation to filter for upward momentum
        self.ema20 = self.I(talib.EMA, self.data.Close, timeperiod=20)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # New: Volume MA for confirmation of conviction in signals
        self.vol_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low = None
        self.div_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < 220:  # Enough for SMA200 + lookback
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1
        current_volume = self.data.Volume[-1]

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation) - Tightened RSI threshold for deeper oversold conditions
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
        )  # Tightened distance and RSI <40 for higher quality setups 🌙
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence - Added oversold confirmation on %D for better entry timing
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (
            (k_now < 20)
            and (k_now > k_prev)
            and (gap_now < gap_prev)
            and (k_now < d_now)
            and (d_now < 30)
        )  # Added %D <30 filter ✨
        if stoch_converge:
            print(
                f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙"
            )

        # Entry Logic - Added volume and EMA20 filters for better signal quality and trend alignment
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and current_price > self.ema20[-1]
            and self.ema20[-1] > self.sma200[-1]
            and current_volume > self.vol_ma[-1]
        ):
            print(f"🌙 Moon Dev: All entry conditions met! Attempting LONG entry... 🚀")
            # Calculate SL: below div low with buffer
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
                self.buy(size=size, sl=sl_price, tp=tp_price)
                self.entry_price = entry_price
                self.sl_price = sl_price
                self.tp_price = tp_price
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, SL: {sl_price}, TP: {tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic - Added trailing stop to lock in profits and improve win rate / returns
        if self.position:
            bars_held = (
                current_bar - self.entry_bar if self.entry_bar is not None else 0
            )
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (
                self.slowk[-1] < self.slowd[-1]
            )

            # New: Trailing stop logic - Update SL if profitable to trail with ATR
            if current_price > self.entry_price:
                new_sl = current_price - (self.atr[-1] * self.trail_mult)
                if new_sl > self.sl_price:
                    self.sl_price = new_sl
                    self.position.sl = new_sl
                    print(f"🌙 Moon Dev: Trailing SL updated to {new_sl} 🚀")

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
bt = Backtest(
    data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True
)
stats = bt.run()
print(stats)
