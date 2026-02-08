# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v6.py
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
    fast_period = 12  # 🌙 Optimized: Kept at 12 for balanced responsiveness on daily BTC
    slow_period = 26  # 🌙 Optimized: Kept at 26 for reliable trend signals
    vol_period = 20  # 🌙 Optimized: Kept at 20 for stable volume filtering
    trend_period = 50  # 🌙 Optimized: Kept at 50 for robust long-term trend confirmation
    risk_pct = 0.02  # 🌙 Improved: Increased from 0.015 to 0.02 to allow higher exposure for targeting 50% returns while maintaining risk control
    atr_period = 14  # Kept: Standard ATR for volatility adjustment
    sl_mult = 2.0  # Kept: ATR multiplier for initial stop loss
    trail_mult = 1.5  # New: ATR multiplier for trailing stop to lock in profits and let winners run longer
    trail_start_mult = 2.0  # New: Start trailing after 2x ATR profit to avoid premature trailing
    vol_mult = 1.2  # 🌙 Improved: Reduced from 1.5 to 1.2 for more entry opportunities without sacrificing quality
    adx_period = 14  # Kept: ADX for trend strength
    adx_threshold = (
        20  # 🌙 Improved: Lowered from 25 to 20 to capture more trending setups for increased trade frequency
    )
    rsi_period = 14  # Kept: RSI for momentum
    rsi_long_thresh = 55  # New: Tightened RSI >55 for long entries to filter for stronger bullish momentum
    rsi_short_thresh = 45  # New: Tightened RSI <45 for short entries to filter for stronger bearish momentum

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Optimized: Retained EMA for quick yet smooth signals
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # Volatility and filters
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print(
            "🌙 Moon Dev Backtest Initialized: Enhanced Bidirectional InverseMomentum Strategy Loaded with Trailing Stops! ✨"
        )

    def next(self):
        # Define crossovers for clarity
        bullish_cross = self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1]
        bearish_cross = self.fast_ema[-2] > self.slow_ema[-2] and self.fast_ema[-1] < self.slow_ema[-1]

        # Debug print every 50 bars (enhanced with crossover info)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f}, "
                f"Bull Cross: {bullish_cross}, Bear Cross: {bearish_cross} 🚀"
            )

        if self.position:
            current_price = self.data.Close[-1]
            # 🌙 Improved: Signal-based exits for both long and short to capture reversals early
            if self.position.is_long and bearish_cross:
                self.position.close()
                print(f"🌙 Moon Dev Long Exit: Bearish crossover detected! Closing at {current_price:.2f} ✨")
            elif self.position.is_short and bullish_cross:
                self.position.close()
                print(f"🌙 Moon Dev Short Exit: Bullish crossover detected! Closing at {current_price:.2f} ✨")

            # 🌙 New: Dynamic trailing stop logic to let winners run while protecting gains (no fixed TP for higher return potential)
            if hasattr(self, "entry_price") and hasattr(self, "entry_atr"):
                if self.position.is_long:
                    if not hasattr(self, "trail_start_long"):
                        self.trail_start_long = self.entry_price + (self.trail_start_mult * self.entry_atr)
                    if current_price > self.trail_start_long:
                        new_sl = current_price - (self.trail_mult * self.atr[-1])
                        if new_sl > self.position.sl:
                            self.position.sl = new_sl
                            print(
                                f"🌙 Moon Dev Trailing SL Update (Long): New SL {new_sl:.2f} at {current_price:.2f} 🚀"
                            )
                elif self.position.is_short:
                    if not hasattr(self, "trail_start_short"):
                        self.trail_start_short = self.entry_price - (self.trail_start_mult * self.entry_atr)
                    if current_price < self.trail_start_short:
                        new_sl = current_price + (self.trail_mult * self.atr[-1])
                        if new_sl < self.position.sl:
                            self.position.sl = new_sl
                            print(
                                f"🌙 Moon Dev Trailing SL Update (Short): New SL {new_sl:.2f} at {current_price:.2f} 🚀"
                            )
        else:
            # 🌙 Improved: Bidirectional entries - added short side for capturing downtrends to boost overall returns
            # Long entry conditions (tightened RSI for better momentum filter)
            if (
                bullish_cross
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.rsi[-1] > self.rsi_long_thresh
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                size = min(size, 1.0)

                self.buy(size=size, sl=sl_price)  # No TP - rely on trailing and signals for extended winners
                self.entry_price = entry_price
                self.entry_atr = self.atr[-1]
                # Reset trailing flag
                if hasattr(self, "trail_start_long"):
                    delattr(self, "trail_start_long")
                print(
                    f"🌙 Moon Dev Long Entry: Bullish momentum confirmed! Vol ({self.vol_mult}x), Trend, RSI {self.rsi[-1]:.1f}> {self.rsi_long_thresh}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, Initial SL: {sl_price:.2f} (Trailing Enabled) 🚀"
                )

            # Short entry conditions (symmetric to long for inverse momentum on downtrends)
            elif (
                bearish_cross
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] < self.trend_sma[-1]
                and self.rsi[-1] < self.rsi_short_thresh
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price + stop_dist
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                size = min(size, 1.0)

                self.sell(size=size, sl=sl_price)  # No TP - rely on trailing and signals
                self.entry_price = entry_price
                self.entry_atr = self.atr[-1]
                # Reset trailing flag
                if hasattr(self, "trail_start_short"):
                    delattr(self, "trail_start_short")
                print(
                    f"🌙 Moon Dev Short Entry: Bearish momentum confirmed! Vol ({self.vol_mult}x), Trend, RSI {self.rsi[-1]:.1f}< {self.rsi_short_thresh}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, Initial SL: {sl_price:.2f} (Trailing Enabled) 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
