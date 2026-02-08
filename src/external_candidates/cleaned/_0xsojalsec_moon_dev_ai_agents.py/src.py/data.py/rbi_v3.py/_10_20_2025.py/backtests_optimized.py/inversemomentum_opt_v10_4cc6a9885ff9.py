# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v10.py
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
    fast_period = 9  # 🌙 Further Optimized: Shortened from 12 to 9 for more responsive signals and increased trade frequency on BTC trends
    slow_period = 21  # 🌙 Further Optimized: Adjusted from 26 to 21 to balance responsiveness without excessive noise
    vol_period = 20  # Retained: Smooth volume average
    trend_period = 50  # Retained: Medium-term trend filter
    long_trend_period = 200  # New: Long-term SMA for bull market confirmation to avoid counter-trend trades
    risk_pct = 0.02  # 🌙 Further Optimized: Increased from 0.015 to 0.02 to allow slightly larger positions for higher return potential
    atr_period = 14  # Retained: Standard ATR
    sl_mult = 1.5  # 🌙 Further Optimized: Tightened from 2.0 to 1.5 for quicker stops, improving win rate and capital preservation
    tp_mult = 5.0  # 🌙 Further Optimized: Increased from 4.0 to 5.0 for better risk-reward (approx 3:1 RR) to capture larger BTC moves
    vol_mult = 1.2  # 🌙 Further Optimized: Reduced from 1.5 to 1.2 to allow more quality entries without sacrificing volume confirmation
    adx_period = 14  # Retained: ADX for trend strength
    adx_threshold = 20  # 🌙 Further Optimized: Lowered from 25 to 20 to include more trending opportunities in BTC's volatile environment
    rsi_period = 14  # Retained: RSI for momentum
    rsi_threshold = 45  # New: Lowered RSI entry from 50 to 45 for earlier momentum capture

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Retained: EMAs for crossover signals, now with fine-tuned periods
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # 🌙 New: Long-term trend filter to ensure trades align with overall bull market in BTC
        self.long_trend_sma = self.I(talib.SMA, close, timeperiod=self.long_trend_period)

        # Retained: Volatility and momentum indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Further Optimized InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring (enhanced with new long-term trend)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} vs Long Trend {self.long_trend_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Further Optimized: Removed premature bearish crossover exit to let winners run to TP/SL, reducing missed large gains in BTC uptrends
            # Instead, rely on ATR-based SL/TP for better risk-reward; add overbought exit if RSI > 80 to protect profits
            if self.rsi[-1] > 80:
                self.position.close()
                print(
                    f"🌙 Moon Dev Exit: Overbought RSI >80 detected! Closing position at {self.data.Close[-1]:.2f} to lock profits ✨"
                )
        else:
            # 🌙 Further Optimized Entry: Bullish EMA crossover + loosened volume (1.2x) + dual trend filters + RSI (>45) + ADX (>20) + new long-term bull filter
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.data.Close[-1] > self.long_trend_sma[-1]
                and self.rsi[-1] > self.rsi_threshold
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Retained: Dynamic position sizing based on ATR, now with higher risk_pct for amplified returns
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                # Cap size to avoid over-leveraging
                size = min(size, 1.0)

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! EMA crossover confirmed with volume ({self.vol_mult}x), "
                    f"trends, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
