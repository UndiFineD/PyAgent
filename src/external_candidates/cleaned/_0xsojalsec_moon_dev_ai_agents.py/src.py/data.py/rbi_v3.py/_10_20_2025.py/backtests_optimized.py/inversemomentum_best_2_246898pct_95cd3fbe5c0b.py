# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_BEST_2.246898pct.py
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

# Resample to daily OHLCV
daily_data = (
    raw_data.resample("1D")
    .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
    .dropna()
)


class InverseMomentum(Strategy):
    fast_period = 12  # 🌙 Optimized: Lengthened from 3 to 12 for fewer whipsaws on daily BTC data
    slow_period = 26  # 🌙 Optimized: Lengthened from 5 to 26, inspired by MACD for better trend capture
    vol_period = 20  # 🌙 Optimized: Increased from 10 to 20 for smoother volume average
    trend_period = 50  # 🌙 Optimized: Increased from 20 to 50 for stronger long-term trend filter
    risk_pct = 0.015  # 🌙 Optimized: Slightly reduced from 0.02 to 0.015 for better risk control while scaling size dynamically
    atr_period = 14  # New: Standard ATR period for volatility-based stops
    sl_mult = 2.0  # New: ATR multiplier for stop loss (2x ATR)
    tp_mult = 4.0  # New: ATR multiplier for take profit (2:1 RR for higher returns)
    vol_mult = 1.5  # 🌙 Optimized: Increased volume threshold from 1x to 1.5x avg for higher quality entries
    adx_period = 14  # New: ADX period for trend strength filter
    adx_threshold = 25  # New: Only enter if ADX > 25 to avoid choppy markets
    rsi_period = 14  # New: RSI period for momentum confirmation

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Optimized: Switched to EMA for faster response to price changes while reducing noise
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)  # SMA fine for volume
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)  # SMA for long-term trend

        # New: Volatility-based indicators for dynamic risk management
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring (enhanced with new indicators)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # Exit on bearish crossover (retained for early reversal detection)
            if self.slow_ema[-2] < self.fast_ema[-2] and self.slow_ema[-1] > self.fast_ema[-1]:
                self.position.close()
                print(f"🌙 Moon Dev Exit: Bearish crossover detected! Closing position at {self.data.Close[-1]:.2f} ✨")
        else:
            # 🌙 Optimized Entry: Bullish EMA crossover + tightened volume (1.5x) + trend filter + new RSI (>50 for momentum) + ADX (>25 for trending market)
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.rsi[-1] > 50
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Optimized: Dynamic position sizing based on ATR for consistent risk % across volatility regimes
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                # Cap size to avoid over-leveraging
                size = min(size, 1.0)

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! EMA crossover confirmed with volume ({self.vol_mult}x), "
                    f"trend, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
