# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v3.py
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
    fast_period = 5  # 🌙 Optimized: Shortened from 12 to 5 for more responsive signals and increased trade frequency on volatile BTC daily data, accepting some whipsaws for higher opportunity capture
    slow_period = 20  # 🌙 Optimized: Adjusted from 26 to 20 to balance responsiveness with trend following, aiming for more entries in BTC's trending phases
    vol_period = 20  # Retained: 20 for smoother volume average
    trend_period = 50  # Retained: 50 for medium-term trend filter
    long_trend_period = 200  # New: Added 200 SMA for long-term bull market filter to avoid entries in major bear phases, enhancing risk-adjusted returns
    risk_pct = 0.02  # 🌙 Optimized: Increased from 0.015 to 0.02 to scale up position sizes modestly, targeting higher compounded returns without excessive risk
    atr_period = 14  # Retained: Standard ATR period
    sl_mult = 2.0  # Retained: ATR multiplier for initial stop loss
    tp_mult = 6.0  # 🌙 Optimized: Increased from 4.0 to 6.0 for a 3:1 risk-reward ratio, allowing winners to run further in BTC's explosive moves to boost overall returns
    vol_mult = 1.2  # 🌙 Optimized: Reduced from 1.5 to 1.2 to allow more qualifying entries without significantly lowering signal quality
    adx_period = 14  # Retained: ADX period
    adx_threshold = 20  # 🌙 Optimized: Lowered from 25 to 20 to include more trending (but not extremely strong) conditions, increasing trade count realistically
    rsi_period = 14  # Retained: RSI period
    trail_trigger_mult = 2.0  # New: ATR multiple to trigger breakeven/trailing (e.g., after 2x ATR profit)
    trail_amount_mult = (
        2.5  # New: ATR multiple for trailing stop distance, tighter than initial SL to lock in gains dynamically
    )

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Retained: EMA for momentum detection
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # New: Long-term trend filter
        self.long_trend = self.I(talib.SMA, close, timeperiod=self.long_trend_period)

        # Retained: Volatility and momentum indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring (added long trend)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} vs Long Trend {self.long_trend[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Optimized: Removed premature bearish crossover exit to let winners run to TP or dynamic SL, improving return potential in trending markets
            # New: Dynamic trailing stop for better profit capture
            entry_price = self.position.entry_price
            current_price = self.data.Close[-1]
            current_atr = self.atr[-1]

            # Trigger trailing if in profit by trail_trigger_mult * ATR
            if current_price > entry_price + self.trail_trigger_mult * current_atr:
                # Calculate new trailing SL
                new_sl = current_price - self.trail_amount_mult * current_atr
                # Only update if it's higher than current SL (move up only for longs)
                if new_sl > self.position.sl:
                    self.position.sl = new_sl
                    print(
                        f"🌙 Moon Dev Trail Update: Moved SL to {new_sl:.2f} (profit lock) at close {current_price:.2f} ✨"
                    )
        else:
            # 🌙 Optimized Entry: Retained bullish EMA crossover, loosened volume (1.2x), RSI (>40 for milder momentum), ADX (>20), added long-term trend filter (>200 SMA)
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.data.Close[-1] > self.long_trend[-1]
                and self.rsi[-1] > 40
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Retained: Dynamic position sizing based on ATR
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
