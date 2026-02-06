# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v10.py
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
    lookback = (
        25  # Increased from 20 to capture more potential divergences for more signals
    )
    recent_period = 12  # Increased from 10 to allow slightly wider recent lows, improving signal frequency
    stoch_window = 7  # Increased from 5 for smoother stochastic convergence detection
    risk_pct = 0.015  # Increased from 0.01 to 1.5% risk per trade for higher exposure while maintaining control
    rr = 3  # Increased from 2 to improve reward potential, aiming for better RR to push towards 50% target
    max_bars = 20  # Increased from 15 to allow positions more time to develop, reducing premature exits
    atr_mult_sl = (
        2.0  # Increased from 1.5 for wider SL to avoid whipsaws in volatile BTC
    )
    buffer_mult = 0.3  # Decreased from 0.5 for tighter buffer around div low, but combined with ATR SL
    adx_threshold = 25  # New: ADX filter for trend strength to avoid choppy markets

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
        self.sma50 = self.I(
            talib.SMA, self.data.Close, timeperiod=50
        )  # New: Shorter SMA for better trend confirmation
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )  # New: ADX for market regime filter
        self.avg_volume = self.I(
            talib.SMA, self.data.Volume, timeperiod=20
        )  # New: Volume SMA for volume confirmation
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.trailing_sl = None  # New: For trailing stop
        self.div_low = None
        self.div_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < 220:  # Enough for SMA200 + lookback
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1
        current_volume = self.data.Volume[-1]
        avg_vol = self.avg_volume[-1]

        # Check if divergence signal still valid
        if self.div_bar is not None and (current_bar - self.div_bar > self.max_bars):
            self.div_bar = None
            self.div_low = None
            print("🌙 Moon Dev: Divergence signal timed out after max_bars. 🔚")

        # RSI Divergence Detection (approximation) - Loosened RSI <50 to <55 for more signals
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
            (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 55) and (distance <= 8)
        )  # Loosened distance from 5 to 8, RSI from 50 to 55
        if (
            bull_div and current_volume > avg_vol * 1.2
        ):  # New: Volume filter - require above-average volume for confirmation
            self.div_low = low2
            self.div_bar = current_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected with volume confirmation! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence - Added oversold condition strengthening
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
        )  # Raised oversold from 20 to 25 for more opportunities
        if stoch_converge:
            print(
                f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙"
            )

        # Entry Logic - Added SMA50 confirmation and ADX filter for better quality setups
        if (
            not self.position
            and self.div_bar is not None
            and stoch_converge
            and current_price > self.sma200[-1]
            and current_price > self.sma50[-1]
            and self.adx[-1] > self.adx_threshold
        ):
            print(
                f"🌙 Moon Dev: All entry conditions met with trend and ADX filters! Attempting LONG entry... 🚀"
            )
            # Improved SL: Use ATR multiple below entry instead of div low for better risk management in trends
            atr_val = self.atr[-1]
            entry_price = current_price
            sl_price = entry_price - (atr_val * self.atr_mult_sl)
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
                self.trailing_sl = sl_price  # Initialize trailing SL
                self.entry_bar = current_bar
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (fraction), Entry: {entry_price}, SL: {sl_price}, TP: {tp_price} 🚀✨"
                )
            else:
                print(f"🌙 Moon Dev: Calculated size {size} <=0, skipping entry. ⚠️")

        # Exit Logic - Added trailing stop based on ATR for profit locking
        if self.position:
            bars_held = (
                current_bar - self.entry_bar if self.entry_bar is not None else 0
            )
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (
                self.slowk[-1] < self.slowd[-1]
            )

            # Update trailing SL: Trail by 1.5 ATR below current price if profitable
            if self.position.is_long and current_price > self.entry_price:
                new_trailing = current_price - (self.atr[-1] * 1.5)
                if new_trailing > self.trailing_sl:
                    self.trailing_sl = new_trailing
                    # In backtesting, manually enforce trailing by closing if below
                    if current_price < self.trailing_sl:
                        self.position.close()
                        print(f"🌙 Moon Dev: Trailing SL hit! EXIT 📉")
                        return

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                return

            # Dynamic exits - Lowered RSI exit to 75 for less aggressive early exits
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                return
            if rsi_now > 75:  # Adjusted from 70 to 75
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >75! EXIT 📈")
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]} ✨ Trailing SL: {self.trailing_sl}"
            )


# Run backtest
bt = Backtest(
    data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True
)
stats = bt.run()
print(stats)
