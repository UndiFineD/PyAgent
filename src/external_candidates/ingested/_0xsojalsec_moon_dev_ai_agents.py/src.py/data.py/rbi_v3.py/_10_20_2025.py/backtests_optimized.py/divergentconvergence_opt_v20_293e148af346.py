# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentConvergence_OPT_v20.py
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
    lookback = 20  # 🌙 Moon Dev Optimization: Increased lookback to 20 for broader historical low detection, improving divergence reliability without overfitting
    recent_period = 10  # 🌙 Moon Dev Optimization: Extended recent period to 10 to capture more recent price action, balancing sensitivity for BTC's volatile swings
    stoch_window = 10  # 🌙 Moon Dev Optimization: Widened stochastic window to 10 for smoother, less noisy convergence signals in 15m timeframe
    risk_pct = 0.02  # 🌙 Moon Dev Optimization: Raised risk per trade to 2% to increase exposure and potential returns, still within conservative risk management for BTC
    rr = 3.0  # 🌙 Moon Dev Optimization: Boosted RR to 3:1 to target higher reward capture in trending BTC moves, enhancing profitability
    max_bars = 40  # 🌙 Moon Dev Optimization: Lengthened max hold time to 40 bars to allow more development in BTC trends, reducing premature time-based exits
    atr_mult_sl = 1.5  # 🌙 Moon Dev Optimization: Tightened trailing ATR multiplier to 1.5 for better profit locking while permitting reasonable volatility breathing room
    buffer_mult = 1.0  # 🌙 Moon Dev Optimization: Increased initial SL buffer multiplier to 1.0 ATR for wider initial stop, avoiding wick-induced stops in BTC's choppy 15m action

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
        # 🌙 Moon Dev Optimization: Retained volume SMA filter but now require >1.1x average for stronger conviction on volume surges
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # 🌙 Moon Dev Optimization: Retained ADX but lowered threshold to 18 for more entries in moderately trending markets, avoiding over-filtering
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        # 🌙 Moon Dev Optimization: Added SMA50 for shorter-term trend confirmation, ensuring entries align with recent uptrends
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low = None
        self.div_bar = None
        self.current_sl = (
            None  # 🌙 Moon Dev Optimization: Track current trailing SL level
        )
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

        bull_div = (
            (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 50) and (distance <= 5)
        )  # 🌙 Moon Dev Optimization: Loosened RSI threshold to <50 for more oversold opportunities and distance to <=5 for slightly fresher, more frequent signals
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
            (k_now < 30)
            and (k_now > k_prev)
            and (gap_now < gap_prev)
            and (k_now < d_now)
        )  # 🌙 Moon Dev Optimization: Raised %K threshold to <30 to capture more convergence setups in BTC's volatile oversold regions
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
            and current_price > self.sma50[-1]
            and self.data.Volume[-1] > 1.1 * self.vol_sma[-1]
            and self.adx[-1] > 18
            and self.data.Close[-1] > self.data.Open[-1]
        ):  # 🌙 Moon Dev Optimization: Added SMA50 confirmation, 1.1x volume threshold, ADX>18, and bullish candle filter for higher-quality, momentum-aligned entries in uptrends
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
            # 🌙 Moon Dev Optimization: Fixed position sizing to properly risk % of current equity: risk_amount = risk_pct * equity, num_units = risk_amount / risk_per_unit, cap by available cash
            risk_amount = self.risk_pct * self.equity
            risk_based_size = risk_amount / risk_per_unit
            available_size = self._broker.cash / entry_price
            size = min(available_size, risk_based_size)
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
                self.div_bar = None
                self.div_low = None
                print(
                    f"🌙 Moon Dev: LONG ENTRY! Size: {size} (units), Entry: {entry_price}, Initial SL: {sl_price}, TP: {tp_price} 🚀✨"
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

            # 🌙 Moon Dev Optimization: Update trailing SL dynamically every bar to lock in profits as price rises
            if self.current_sl is None:
                self.current_sl = self.sl_price
            new_trail_sl = current_price - (self.atr[-1] * self.atr_mult_sl)
            self.current_sl = max(self.current_sl, new_trail_sl)

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                self.current_sl = None
                return

            # Stochastic cross exit
            if k_cross_below_d:
                self.position.close()
                print(f"🌙 Moon Dev: Stochastic %K crossed below %D! EXIT 📉")
                self.current_sl = None
                return

            # RSI overbought exit
            if rsi_now > 70:
                self.position.close()
                print(f"🌙 Moon Dev: RSI Overbought >70! EXIT 📈")
                self.current_sl = None
                return

            # Trailing SL check
            if current_price < self.current_sl:
                self.position.close()
                print(f"🌙 Moon Dev: Trailing SL hit at {current_price}! 📉")
                self.current_sl = None
                return

            print(
                f"🌙 Moon Dev: Position held. Bars: {bars_held}, Price: {current_price}, RSI: {rsi_now}, %K: {self.slowk[-1]}, Trail SL: {self.current_sl} ✨"
            )


# Run backtest
bt = Backtest(
    data, DivergentConvergence, cash=1000000, commission=0.002, exclusive_orders=True
)
stats = bt.run()
print(stats)
