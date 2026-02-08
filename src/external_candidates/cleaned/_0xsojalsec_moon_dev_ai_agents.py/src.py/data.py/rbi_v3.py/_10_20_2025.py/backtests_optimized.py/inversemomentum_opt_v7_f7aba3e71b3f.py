# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v7.py
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
raw_data = raw_data.drop(columns=[col for col in raw_data.columns if "unnamed" in col.lower()])

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

# 🌙 Optimized: Use 15m data instead of daily resample for higher trade frequency and potential returns on BTC's intraday volatility
# This allows more opportunities to capture momentum swings while filters prevent overtrading


class InverseMomentum(Strategy):
    fast_period = (
        8  # 🌙 Optimized: Shortened to 8 for 15m TF to capture quicker momentum shifts without excessive noise
    )
    slow_period = 21  # 🌙 Optimized: Set to 21 (Fibonacci) for better trend alignment on shorter timeframe
    vol_period = 14  # 🌙 Optimized: Reduced to 14 for more responsive volume averaging on 15m
    trend_period = 100  # 🌙 Optimized: Adjusted to 100 for medium-term trend filter suitable for 15m (approx 1-2 days)
    risk_pct = (
        0.02  # 🌙 Optimized: Increased from 0.015 to 0.02 to scale up returns while keeping risk per trade controlled
    )
    atr_period = 14  # Retained: Standard ATR for volatility
    sl_mult = 2.0  # Retained: 2x ATR for stop loss
    tp_mult = 5.0  # 🌙 Optimized: Increased from 4.0 to 5.0 for improved 2.5:1 RR to boost average win size and hit target returns
    vol_mult = 1.2  # 🌙 Optimized: Reduced from 1.5 to 1.2 to allow more quality entries without being too restrictive on 15m volume spikes
    adx_period = 14  # Retained: ADX for trend strength
    adx_threshold = (
        30  # 🌙 Optimized: Increased from 25 to 30 for stronger trend confirmation, reducing false signals in chop
    )
    rsi_period = 14  # Retained: RSI for momentum

    # 🌙 New: Add longer-term trend filter for regime awareness
    long_trend_period = 200  # Approx 2-3 days on 15m for overall bull bias

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Retained: EMA for responsive signals
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # 🌙 Retained: Volatility and momentum indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # 🌙 New: Long-term SMA for bull market regime filter to avoid counter-trend trades
        self.long_trend_sma = self.I(talib.SMA, close, timeperiod=self.long_trend_period)

        # 🌙 New: ATR SMA for volatility regime filter - only trade in expanding volatility for better setups
        self.atr_sma = self.I(talib.SMA, self.atr, timeperiod=20)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy on 15m Loaded! ✨")

    def next(self):
        # Debug print every 100 bars for monitoring on higher frequency data (adjusted from 50)
        if len(self.data) % 100 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} vs Long {self.long_trend_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f} vs Avg {self.atr_sma[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Optimized: Removed bearish crossover exit to let winners run longer, relying on trailing potential via SL/TP for higher returns
            # This prevents premature exits in strong trends, key for targeting 50%+
            pass  # No manual close; use SL/TP only
        else:
            # 🌙 Optimized Entry: Retained core + new long-term trend (>200 SMA) and volatility filter (ATR > avg for expanding vol)
            # Slightly loosened vol_mult to 1.2 and raised ADX to 30 for balanced frequency/quality on 15m
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.data.Close[-1] > self.long_trend_sma[-1]  # New: Bull regime filter
                and self.rsi[-1] > 50
                and self.adx[-1] > self.adx_threshold
                and self.atr[-1] > self.atr_sma[-1]
            ):  # New: Trade only in rising volatility regimes for better momentum follow-through
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Retained: Dynamic sizing for consistent risk
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                # 🌙 Optimized: Increased cap to 1.5 to allow slight over-allocation in low-vol setups for return boost
                size = min(size, 1.5)

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC 15m! EMA crossover with volume ({self.vol_mult}x), "
                    f"trends, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}, Vol Regime Confirmed. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest on 15m data
bt = Backtest(raw_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
