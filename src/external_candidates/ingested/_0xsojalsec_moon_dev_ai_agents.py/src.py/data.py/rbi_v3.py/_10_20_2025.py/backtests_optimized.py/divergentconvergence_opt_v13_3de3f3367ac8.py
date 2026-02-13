# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v13.py
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
    lookback = 30  # Optimized: Increased from 20 to 30 for capturing more robust historical lows in divergence detection 🌙
    recent_period = 15  # Optimized: Increased from 10 to 15 to allow for slightly broader recent swing analysis without losing relevance ✨
    stoch_window = 8  # Optimized: Increased from 5 to 8 for smoother stochastic convergence signals 🚀
    risk_pct = 0.015  # Optimized: Increased from 0.01 to 0.015 for slightly more aggressive position sizing to boost returns while keeping risk controlled 📈
    rr = 2.5  # Optimized: Increased from 2 to 2.5 to improve risk-reward ratio for higher profitability on winning trades 💰
    max_bars = 25  # Optimized: Increased from 15 to 25 to allow trades more time to develop in volatile BTC markets ⏱️
    atr_mult_sl = 1.5
    buffer_mult = 0.5
    trail_mult = (
        2.5  # New: Trailing stop multiplier based on ATR for dynamic profit locking 🌙
    )

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        # Optimized: Adjusted Stochastic to faster period (8,3,3) from (14,3,3) for quicker oversold convergence detection in 15m timeframe ⚡
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
        # New: Added SMA20 for short-term uptrend filter to confirm momentum before entry 📊
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        # New: Added Volume SMA for confirmation of increasing participation on signals 🔊
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # New: Added ADX for trend strength filter to avoid choppy markets and focus on favorable regimes 🌟
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.entry_bar = None
        self.entry_price = None
        self.initial_sl = None  # New: For initial risk calculation only
        self.tp_price = None
        self.trail_sl = None  # New: Dynamic trailing stop level
        self.div_low = None
        self.div_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if (
            len(self.data) < 250
        ):  # Optimized: Increased buffer to 250 to accommodate new indicators like SMA200 + ADX + extras 🔍
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1

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

        # Optimized: Removed distance <=5 constraint to capture more divergence signals without being too restrictive 🎯
        bull_div = (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 50)
        if bull_div:
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence
        # Optimized: Loosened oversold threshold to <30 from <20 to generate more convergence opportunities in BTC volatility 📈
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (
            (k_now < 30)
            and (k_now > k_prev)
            and (gap_now < gap_prev)
            and (k_now < d_now)
        )
        if stoch_converge:
            print(
                f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙"
            )

        # Entry Logic
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and current_price > self.sma20[-1]
            and self.data.Volume[-1] > self.vol_sma[-1]
            and self.adx[-1] > 20
        ):
            print(f"🌙 Moon Dev: All entry conditions met! Attempting LONG entry... 🚀")
            # Calculate initial SL for risk sizing: below div low with buffer
            div_low = self.div_low
            atr_val = self.atr[-1]
            initial_sl = div_low - (atr_val * self.buffer_mult)
            entry_price = current_price
            risk_per_unit = entry_price - initial_sl
            if risk_per_unit <= 0:
                print(
                    f"🌙 Moon Dev: Invalid risk per unit: {risk_per_unit}, skipping entry. ⚠️"
                )
                return
            size_frac = self.risk_pct * entry_price / risk_per_unit
            size = min(1.0, size_frac)
            if size > 0:
                self.buy(
                    size=size
                )  # Optimized: Removed fixed sl/tp from buy; now handled dynamically in next() for trailing and better exits 🔄
                self.entry_price = entry_price
                self.initial_sl = initial_sl
                self.tp_price = entry_price + self.rr * risk_per_unit
                self.trail_sl = initial_sl  # Initialize trailing SL
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, Initial SL: {initial_sl}, TP: {self.tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic
        if self.position:
            bars_held = (
                current_bar - self.entry_bar if self.entry_bar is not None else 0
            )
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (
                self.slowk[-1] < self.slowd[-1]
            )

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                return

            # Fixed TP hit
            if current_price >= self.tp_price:
                self.position.close()
                print(f"🌙 Moon Dev: Take Profit HIT at {self.tp_price}! 🚀💰")
                return

            # Optimized: Dynamic trailing stop implementation to lock in profits as price moves favorably 📊
            atr_val = self.atr[-1]
            new_trail = current_price - (atr_val * self.trail_mult)
            if new_trail > self.trail_sl:
                self.trail_sl = new_trail
                print(f"🌙 Moon Dev: Trailing SL updated to {self.trail_sl} ✨")

            # Trailing SL hit
            if self.data.Low[-1] <= self.trail_sl:
                self.position.close()
                print(f"🌙 Moon Dev: Trailing SL HIT at {self.trail_sl}! 📉")
                return

            # Other signal-based exits
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
