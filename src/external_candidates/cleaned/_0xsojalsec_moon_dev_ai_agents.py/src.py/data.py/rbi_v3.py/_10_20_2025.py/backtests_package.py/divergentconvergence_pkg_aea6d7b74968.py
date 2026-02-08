# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_package\DivergentConvergence_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data loading and cleaning
path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path, index_col=0, parse_dates=True)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class DivergentConvergence(Strategy):
    pivot_window = 5  # Not used, using approximation
    lookback = 20
    recent_period = 10
    stoch_window = 5
    risk_pct = 0.01
    rr = 2
    max_bars = 15
    atr_mult_sl = 1.5
    buffer_mult = 0.5

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.slowk, self.slowd = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.entry_bar = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.div_low_bar = None
        print("🌙 Moon Dev Backtest Initialized! ✨ Initializing indicators... 🚀")

    def next(self):
        if len(self.data) < self.lookback + 10:
            return

        current_price = self.data.Close[-1]
        current_bar = len(self.data) - 1

        # RSI Divergence Detection (approximation)
        lows_recent = self.data.Low.s.iloc[-self.lookback :]
        rsi_recent = self.rsi.s.iloc[-self.lookback :]
        low1 = lows_recent.iloc[: self.recent_period].min()
        rsi1 = rsi_recent.iloc[: self.recent_period].min()
        low2 = lows_recent.iloc[self.recent_period :].min()
        rsi2 = rsi_recent.iloc[self.recent_period :].min()

        low2_bar = self.data.Low.s.iloc[-self.recent_period :].idxmin()
        distance = current_bar - low2_bar

        bull_div = (low2 < low1) and (rsi2 > rsi1) and (rsi2 < 50) and (distance <= 5)
        if bull_div:
            self.div_low_bar = low2_bar
            print(
                f"🌙 Moon Dev: Bullish RSI Divergence detected! Price low: {low2}, RSI: {rsi2} ✨ Distance: {distance} bars"
            )

        # Stochastic Convergence
        if len(self.slowk) < self.stoch_window + 3:
            return
        k_now = self.slowk[-1]
        d_now = self.slowd[-1]
        k_prev = self.slowk[-self.stoch_window]
        d_prev = self.slowd[-self.stoch_window]
        gap_now = abs(d_now - k_now)
        gap_prev = abs(d_prev - k_prev)
        stoch_converge = (k_now < 20) and (k_now > k_prev) and (gap_now < gap_prev) and (k_now < d_now)
        if stoch_converge:
            print(f"🚀 Moon Dev: Stochastic Convergence! %K: {k_now}, %D: {d_now}, Gap narrowed! 🌙")

        # Entry Logic
        if not self.position and bull_div and stoch_converge and current_price > self.sma200[-1]:
            # Calculate SL: below div low with buffer
            div_low = self.data.Low[self.div_low_bar]
            atr_val = self.atr[-1]
            sl_price = div_low - (atr_val * self.buffer_mult)
            entry_price = current_price
            risk_per_unit = entry_price - sl_price
            risk_amount = self.equity * self.risk_pct
            position_size = risk_amount / risk_per_unit
            size = int(round(position_size))
            self.buy(size=size)
            self.entry_price = entry_price
            self.sl_price = sl_price
            self.tp_price = entry_price + self.rr * risk_per_unit
            self.entry_bar = current_bar
            print(
                f"🌙 Moon Dev: LONG ENTRY! Size: {size}, Entry: {entry_price}, SL: {sl_price}, TP: {self.tp_price} 🚀✨"
            )

        # Exit Logic
        if self.position:
            bars_held = current_bar - self.entry_bar if self.entry_bar is not None else 0
            low_now = self.data.Low[-1]
            high_now = self.data.High[-1]
            rsi_now = self.rsi[-1]
            k_cross_below_d = (self.slowk[-2] >= self.slowd[-2]) and (self.slowk[-1] < self.slowd[-1])

            # Time-based exit
            if bars_held > self.max_bars:
                self.position.close()
                print(f"🌙 Moon Dev: Time-based EXIT after {bars_held} bars! 😴")
                return

            # Stop Loss
            if low_now <= self.sl_price:
                self.position.close()
                print(f"🌙 Moon Dev: STOP LOSS hit at {low_now}! 💥")
                return

            # Take Profit
            if high_now >= self.tp_price:
                self.position.close()
                print(f"🌙 Moon Dev: TAKE PROFIT hit at {high_now}! 💰🚀")
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
