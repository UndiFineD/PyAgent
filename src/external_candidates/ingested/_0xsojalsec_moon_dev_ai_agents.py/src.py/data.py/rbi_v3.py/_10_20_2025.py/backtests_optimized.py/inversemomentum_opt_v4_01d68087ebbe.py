# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v4.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
raw_data = pd.read_csv(data_path)

# Clean column names
raw_data.columns = raw_data.columns.str.strip().str.lower()

# Drop unnamed columns
raw_data = raw_data.drop(
    columns=[col for col in raw_data.columns if "unnamed" in col.lower()]
)

# Rename columns properly (keep datetime lowercase for set_index)
raw_data = raw_data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Convert to datetime and set index
raw_data["datetime"] = pd.to_datetime(raw_data["datetime"])
raw_data = raw_data.set_index(raw_data["datetime"]).drop("datetime", axis=1)

# Resample to daily OHLCV
daily_data = (
    raw_data.resample("1D")
    .agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    .dropna()
)


class InverseMomentum(Strategy):
    fast_period = 10  # 🌙 Optimized: Shortened from 12 to 10 for more responsive signals on volatile BTC daily data, increasing trade frequency realistically
    slow_period = 25  # 🌙 Optimized: Adjusted from 26 to 25 to align better with Fibonacci for natural market cycles
    vol_period = 20  # Kept: Smooth volume average works well
    trend_period = 50  # Kept: Strong medium-term trend filter
    long_trend_period = 200  # New: Long-term SMA filter to ensure entries only in overall uptrend, avoiding major bear markets
    risk_pct = 0.02  # 🌙 Optimized: Increased from 0.015 to 0.02 for higher exposure and returns while keeping risk managed
    atr_period = 14  # Kept: Standard for volatility
    sl_mult = 2.0  # Kept: Balanced initial stop
    tp_mult = 5.0  # 🌙 Optimized: Increased from 4.0 to 5.0 for higher reward:risk (2.5:1), targeting bigger wins in BTC trends
    vol_mult = 1.2  # 🌙 Optimized: Loosened from 1.5 to 1.2 for more qualifying volume spikes without sacrificing quality
    adx_period = 14  # Kept: For trend strength
    adx_threshold = 20  # 🌙 Optimized: Lowered from 25 to 20 to capture more trending opportunities in crypto
    rsi_period = 14  # Kept: Momentum confirmation
    rsi_threshold = (
        45  # New: Slightly lowered from 50 to 45 for more bullish momentum entries
    )
    trail_mult = 1.5  # New: Multiplier for trailing stop (tighter than initial SL to lock profits)
    profit_start_mult = (
        1.0  # New: Start trailing after 1x ATR profit to let small moves breathe
    )

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Optimized: Retained EMA for responsiveness, with adjusted periods
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)
        # New: Long-term trend filter for regime awareness
        self.long_sma = self.I(talib.SMA, close, timeperiod=self.long_trend_period)

        # Volatility and momentum indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Position management variables
        self.entry_price = None
        self.tp_price = None
        self.trail_sl = None
        self.initial_atr = None

        # Debug print on init
        print(
            "🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy with Trailing Stops Loaded! ✨"
        )

    def next(self):
        # Debug print every 50 bars for monitoring (enhanced with new long-term trend)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1]/self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} vs Long {self.long_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        # 🌙 Optimized: Manage existing position first with trailing stop, TP, SL, and crossover exit for better profit capture
        if self.position:
            closed = False
            # Bearish crossover exit for early reversal
            if (
                self.slow_ema[-2] < self.fast_ema[-2]
                and self.slow_ema[-1] > self.fast_ema[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev Exit: Bearish crossover detected! Closing at {self.data.Close[-1]:.2f} ✨"
                )
                closed = True
            # TP check
            elif self.data.Close[-1] >= self.tp_price:
                self.position.close()
                print(
                    f"🌙 Moon Dev TP Hit: Reached {self.tp_price:.2f} at close {self.data.Close[-1]:.2f}! 🚀"
                )
                closed = True
            # Update trailing SL if in profit
            elif (
                self.data.Close[-1]
                > self.entry_price + self.profit_start_mult * self.atr[-1]
            ):
                new_trail = self.data.Close[-1] - self.trail_mult * self.atr[-1]
                self.trail_sl = max(self.trail_sl, new_trail)
            # SL check using Low for realism
            if self.data.Low[-1] <= self.trail_sl:
                self.position.close()
                print(
                    f"🌙 Moon Dev SL Hit: Trailing SL triggered at {self.trail_sl:.2f} (Low: {self.data.Low[-1]:.2f}) 💥"
                )
                closed = True

            # Reset variables on close
            if closed:
                self.entry_price = None
                self.tp_price = None
                self.trail_sl = None
                self.initial_atr = None

        # Entry logic only if no position
        if not self.position:
            # 🌙 Optimized Entry: Bullish EMA crossover + loosened volume (1.2x) + dual trend filters + RSI (>45) + ADX (>20) + long-term uptrend
            if (
                (
                    self.fast_ema[-2] < self.slow_ema[-2]
                    and self.fast_ema[-1] > self.slow_ema[-1]
                )
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.data.Close[-1] > self.long_sma[-1]
                and self.rsi[-1] > self.rsi_threshold
                and self.adx[-1] > self.adx_threshold
            ):

                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Optimized: Dynamic sizing with increased risk_pct for higher returns
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                size = min(size, 1.0)  # Cap to prevent overexposure

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size)
                self.entry_price = entry_price
                self.tp_price = tp_price
                self.trail_sl = sl_price
                self.initial_atr = self.atr[-1]
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! EMA crossover with volume ({self.vol_mult}x), "
                    f"trends, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, Initial SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(
    daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True
)

stats = bt.run()
print(stats)
print(stats._strategy)
