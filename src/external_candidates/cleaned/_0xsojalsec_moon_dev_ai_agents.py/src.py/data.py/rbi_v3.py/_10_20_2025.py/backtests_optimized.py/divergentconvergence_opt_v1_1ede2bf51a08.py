# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v1.py
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
    risk_pct = 0.02  # 🌙 Moon Dev Optimization: Increased risk per trade from 1% to 2% for higher exposure while maintaining risk management
    rr = 3  # 🌙 Moon Dev Optimization: Increased RR from 2 to 3 for better reward potential on winning trades
    max_bars = 25  # 🌙 Moon Dev Optimization: Extended max hold time from 15 to 25 bars to allow more room for trends to develop
    atr_mult_sl = 1.5
    buffer_mult = 0.5
    trail_start_mult = (
        1.5  # 🌙 Moon Dev Optimization: New parameter for when to start trailing stop (after 1.5 ATR profit)
    )
    trail_atr_mult = 2.0  # 🌙 Moon Dev Optimization: Trailing stop distance as 2 ATR below current price

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
        # 🌙 Moon Dev Optimization: Added volume SMA for volume confirmation filter to avoid low-volume entries
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # 🌙 Moon Dev Optimization: Added ADX for trend strength filter to only enter in trending markets (ADX > 20)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
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

        # 🌙 Moon Dev Optimization: Tightened distance condition from <=5 to <=3 for higher-quality, more recent divergences
        bull_div = (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 50) and (distance <= 3)
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
        # 🌙 Moon Dev Optimization: Lowered %K threshold from <20 to <15 for stronger oversold condition
        stoch_converge = (k_now < 15) and (k_now > k_prev) and (gap_now < gap_prev) and (k_now < d_now)
        if stoch_converge:
            print(f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙")

        # Entry Logic
        if not self.position and self.div_bar is not None and stoch_converge and current_price > self.sma200[-1]:
            # 🌙 Moon Dev Optimization: Added volume and ADX filters for better entry quality - higher volume and trending market
            vol_confirm = self.data.Volume[-1] > self.vol_sma[-1] * 1.1  # Current volume > 1.1x 20-period avg
            trend_confirm = self.adx[-1] > 20  # ADX >20 indicates sufficient trend strength
            if vol_confirm and trend_confirm:
                print(f"🌙 Moon Dev: All entry conditions met including volume & ADX! Attempting LONG entry... 🚀")
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
                    print(f"🌙 Moon Dev: Volume confirm: {vol_confirm}, ADX: {self.adx[-1]} 📊")
                else:
                    print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")
            else:
                print(
                    f"🌙 Moon Dev: Entry blocked by filters - Vol: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}x avg, ADX: {self.adx[-1]} ⚠️"
                )

        # Exit Logic
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])
            atr_val = self.atr[-1]

            # 🌙 Moon Dev Optimization: Added trailing stop logic - activates after 1.5 ATR profit, trails at 2 ATR below current price
            if current_price > self.entry_price + (atr_val * self.trail_start_mult):
                trail_sl = current_price - (atr_val * self.trail_atr_mult)
                if trail_sl > self.sl_price:
                    self.position.sl = trail_sl
                    self.sl_price = trail_sl
                    print(
                        f"🌙 Moon Dev: Trailing SL updated to {trail_sl} (from {self.entry_price + (atr_val * self.trail_start_mult)} profit threshold) 🔄"
                    )

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
