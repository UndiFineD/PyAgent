# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v5.py
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
    fast_period = 10  # 🌙 Optimized: Shortened to 10 from 12 for more responsive entries on BTC daily, capturing earlier momentum shifts
    slow_period = 30  # 🌙 Optimized: Extended to 30 from 26 for better trend separation, reducing false signals in volatile crypto
    vol_period = 14  # 🌙 Optimized: Reduced to 14 from 20 for quicker volume confirmation, allowing more timely entries
    trend_period = 100  # 🌙 Optimized: Increased to 100 from 50 for a medium-term trend filter, ensuring alignment with broader uptrends
    lt_trend_period = (
        200  # New: Long-term SMA for overall bull market filter, only trade longs in uptrends to boost win rate
    )
    risk_pct = (
        0.02  # 🌙 Optimized: Increased to 0.02 from 0.015 to scale up returns while keeping risk per trade controlled
    )
    atr_period = 14  # Retained: Standard ATR for volatility
    sl_mult = 1.5  # 🌙 Optimized: Tightened to 1.5x ATR from 2.0 for closer stops, enabling larger position sizes and better risk-reward
    tp_mult = 5.0  # 🌙 Optimized: Increased to 5.0x ATR from 4.0 for higher reward potential (3.33:1 RR), aiming for bigger winners
    vol_mult = 1.2  # 🌙 Optimized: Loosened to 1.2x from 1.5x avg volume to increase trade frequency without sacrificing quality
    adx_period = 14  # Retained: ADX for trend strength
    adx_threshold = (
        20  # 🌙 Optimized: Lowered to 20 from 25 to capture more trending opportunities in BTC's volatile regimes
    )
    rsi_period = 14  # Retained: RSI for momentum
    rsi_threshold = 45  # New: Lowered RSI entry to >45 from 50 for earlier momentum confirmation, filtering out oversold but adding trades
    trail_mult = 2.0  # New: ATR multiplier for trailing stop distance from recent high

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Retained EMAs with optimized periods for balanced responsiveness
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)
        # New: Long-term trend filter to avoid counter-trend trades in bear markets
        self.lt_trend = self.I(talib.SMA, close, timeperiod=self.lt_trend_period)

        # Retained volatility indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring (enhanced with new LT trend)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} vs LT {self.lt_trend[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Retained: Exit on bearish crossover for early reversal protection
            if self.slow_ema[-2] < self.fast_ema[-2] and self.slow_ema[-1] > self.fast_ema[-1]:
                self.position.close()
                print(f"🌙 Moon Dev Exit: Bearish crossover detected! Closing position at {self.data.Close[-1]:.2f} ✨")

            # New: Trailing stop implementation for capturing larger trends
            if not hasattr(self, "trailing_sl"):
                self.trailing_sl = self.position.sl  # Initialize from initial SL
            # Update trailing SL based on recent high minus trail distance
            potential_trail = self.data.High[-1] - (self.trail_mult * self.atr[-1])
            if potential_trail > self.trailing_sl:
                self.trailing_sl = potential_trail
                self.position.sl = self.trailing_sl  # Update the position's SL
                print(
                    f"🌙 Moon Dev Trailing Update: New SL at {self.trailing_sl:.2f} (High: {self.data.High[-1]:.2f}, ATR: {self.atr[-1]:.2f}) 🚀"
                )

            # Exit if price hits trailing SL (redundant but ensures)
            if self.data.Close[-1] < self.trailing_sl:
                self.position.close()
                print(f"🌙 Moon Dev Exit: Trailing stop hit at {self.data.Close[-1]:.2f} ✨")
        else:
            # 🌙 Optimized Entry: Bullish EMA crossover + loosened volume (1.2x) + dual trend filters (medium + LT) + RSI (>45) + ADX (>20)
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.data.Close[-1] > self.lt_trend[-1]  # New: LT trend filter for bull market only
                and self.rsi[-1] > self.rsi_threshold
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Retained: Dynamic position sizing based on ATR, now with higher risk_pct and tighter SL for larger sizes
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                size = min(size, 1.0)  # Cap to avoid over-leveraging

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                self.trailing_sl = sl_price  # Initialize trailing for this position
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
